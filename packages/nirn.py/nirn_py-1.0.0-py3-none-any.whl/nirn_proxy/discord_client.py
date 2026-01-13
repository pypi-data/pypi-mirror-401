"""Discord HTTP client for making rate-limited requests."""
import asyncio
import aiohttp
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from .config import Config
from .bucket_path import get_metrics_path
from .metrics import request_histogram
from .util import has_auth_prefix


@dataclass
class DiscordResponse:
    """Response wrapper to allow reading body multiple times."""
    status: int
    status_text: str
    headers: Dict[str, str]
    body: bytes
    
    async def json(self) -> Any:
        import json
        return json.loads(self.body)
    
    async def text(self) -> str:
        return self.body.decode('utf-8')
    
    async def read(self) -> bytes:
        return self.body


class DiscordClient:
    """
    Discord HTTP client for making rate-limited API requests.
    
    Key features:
    - Configurable transport settings
    - Returns response bodies that can be read multiple times
    - Handles request timeout
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.context_timeout = config.request_timeout / 1000  # Convert ms to seconds
        
    async def __aenter__(self):
        """Create HTTP client with configured transport settings."""
        connector_kwargs = {
            "limit": 1000,  # MaxIdleConns
            "limit_per_host": 0,  # No per-host limit
            "enable_cleanup_closed": True,
        }
        
        # Disable HTTP/2 if requested (force_close and keepalive_timeout are mutually exclusive)
        if self.config.disable_http_2:
            connector_kwargs["force_close"] = True
        else:
            connector_kwargs["keepalive_timeout"] = 90  # IdleConnTimeout
            connector_kwargs["force_close"] = False
        
        # Bind to specific outbound IP if configured
        if self.config.outbound_ip:
            connector_kwargs["local_addr"] = (self.config.outbound_ip, 0)
        
        connector = aiohttp.TCPConnector(**connector_kwargs)
        
        # Create session with 90 second total timeout
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=90),
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def do_discord_request(
        self,
        path: str,
        method: str,
        body: Optional[bytes],
        headers: Dict[str, str],
        query: str,
        identifier: str = "Internal"
    ) -> DiscordResponse:
        """
        Make a request to Discord API.
        
        Uses context timeout for the actual request, but session has 90s total timeout.
        """
        url = f"https://discord.com{path}"
        if query:
            url += f"?{query}"
        
        start_time = time.time()
        
        try:
            # Use context timeout like Go
            timeout = aiohttp.ClientTimeout(total=self.context_timeout)
            
            async with self.session.request(
                method, 
                url, 
                headers=headers, 
                data=body,
                timeout=timeout
            ) as resp:
                # Read body immediately so we can return a reusable response
                response_body = await resp.read()
                
                # Record metrics
                route = get_metrics_path(path)
                status = f"{resp.status} {resp.reason}"
                elapsed = time.time() - start_time
                
                if resp.status == 429:
                    scope = resp.headers.get("x-ratelimit-scope", "")
                    if scope == "shared":
                        status = "429 Shared"
                
                request_histogram.labels(
                    route=route,
                    status=status,
                    method=method,
                    clientId=identifier
                ).observe(elapsed)
                
                return DiscordResponse(
                    status=resp.status,
                    status_text=resp.reason or "",
                    headers=dict(resp.headers),
                    body=response_body
                )
                
        except asyncio.TimeoutError:
            elapsed = time.time() - start_time
            route = get_metrics_path(path)
            request_histogram.labels(
                route=route,
                status="Timeout",
                method=method,
                clientId=identifier
            ).observe(elapsed)
            raise
        except Exception as e:
            elapsed = time.time() - start_time
            route = get_metrics_path(path)
            request_histogram.labels(
                route=route,
                status="Error",
                method=method,
                clientId=identifier
            ).observe(elapsed)
            raise
    
    async def make_request(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        body: Optional[bytes] = None,
        query: str = "",
        identifier: str = "Internal"
    ) -> DiscordResponse:
        """
        Process a request to Discord.
        
        This is the main entry point for queue processing.
        """
        return await self.do_discord_request(path, method, body, headers, query, identifier)
    
    async def get_bot_user(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get bot user information.
        
        Returns None for 401/not found, raises for 429/500.
        """
        headers = {"Authorization": token}
        
        try:
            resp = await self.do_discord_request(
                "/api/v9/users/@me", 
                "GET", 
                None, 
                headers, 
                ""
            )
            
            if resp.status == 401:
                return None
            elif resp.status == 429:
                raise Exception("429 on users/@me")
            elif resp.status == 500:
                raise Exception("500 on users/@me")
            
            return await resp.json()
            
        except Exception as e:
            if "429" in str(e) or "500" in str(e):
                raise
            return None
    
    async def get_bot_gateway(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get bot gateway information from /gateway/bot.
        
        Returns session_start_limit data for calculating global limit.
        """
        headers = {"Authorization": token}
        
        resp = await self.do_discord_request(
            "/api/v9/gateway/bot",
            "GET",
            None,
            headers,
            ""
        )
        
        if resp.status == 401:
            # Return math.MaxUint32 equivalent for invalid token to fail fast
            raise Exception("invalid token - nirn.py")
        elif resp.status == 429:
            raise Exception("429 on gateway/bot")
        elif resp.status == 500:
            raise Exception("500 on gateway/bot")
        
        return await resp.json()
    
    def get_bot_global_limit(
        self, 
        token: str, 
        user_data: Optional[Dict], 
        gateway_data: Optional[Dict]
    ) -> int:
        """
        Calculate bot global limit.
        
        Logic:
        - No token: max int
        - Override exists: use override
        - Bearer: 50
        - Basic: 50
        - Detection disabled: 50
        - Based on concurrency: max(500, 25 * concurrency) or 50 if concurrency == 1
        """
        import math
        
        if not token:
            return 2**31 - 1  # math.MaxUint32 equivalent
        
        # Check for overrides
        if user_data and user_data.get("id") in self.config.bot_override_map:
            return self.config.bot_override_map[user_data["id"]]
        
        if has_auth_prefix(token, "Bearer"):
            return 50
        
        if has_auth_prefix(token, "Basic"):
            return 50
        
        if self.config.disable_global_ratelimit_detection:
            return 50
        
        if not gateway_data:
            return 50
        
        # Calculate based on concurrency
        session_limit = gateway_data.get("session_start_limit", {})
        concurrency = session_limit.get("max_concurrency", 1)
        
        if concurrency == 1:
            return 50
        else:
            limit = 25 * concurrency
            if limit > 500:
                return limit
            return 500