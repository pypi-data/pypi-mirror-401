"""Distributed global rate limiter for cluster-wide rate limit coordination."""
import asyncio
import logging
import time
from typing import Dict, Optional
import aiohttp
from .leaky_bucket import LeakyBucket


logger = logging.getLogger(__name__)


class ClusterGlobalRateLimiter:
    """
    Distributed global rate limiter for cluster coordination.
    
    Uses leaky bucket rate limiting per bot hash to enforce global rate limits
    across the cluster.
    """
    
    def __init__(self):
        # Map of bot_hash -> LeakyBucket
        self.global_buckets_map: Dict[int, LeakyBucket] = {}
        self._lock = asyncio.Lock()
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Initialize HTTP session for cluster communication."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30.0)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup HTTP session."""
        if self.session:
            await self.session.close()
    
    async def _get_or_create(self, bot_hash: int, bot_limit: int) -> LeakyBucket:
        """
        Get or create a bucket for a bot.
        
        Uses double-checked locking pattern.
        """
        # Check with read lock (simulated by checking without lock first)
        if bot_hash in self.global_buckets_map:
            return self.global_buckets_map[bot_hash]
        
        async with self._lock:
            # Double-check after acquiring lock
            if bot_hash in self.global_buckets_map:
                return self.global_buckets_map[bot_hash]
            
            # Create new bucket
            bucket = LeakyBucket(
                name=str(bot_hash),
                capacity=bot_limit,
                period=1.0  # 1 second window
            )
            self.global_buckets_map[bot_hash] = bucket
            return bucket
    
    async def take(self, bot_hash: int, bot_limit: int) -> None:
        """
        Take a global rate limit token.
        
        This blocks until a token is available.
        """
        bucket = await self._get_or_create(bot_hash, bot_limit)
        
        while True:
            success = await bucket.add(1)
            if success:
                return
            
            # Wait until bucket resets
            reset_time = bucket.reset_time()
            wait_time = reset_time - time.time()
            
            if wait_time > 0:
                logger.debug(f"Failed to grab global token, sleeping for a bit - waitTime: {wait_time}")
                await asyncio.sleep(wait_time)
    
    async def fire_global_request(self, addr: str, bot_hash: int, bot_limit: int) -> None:
        """
        Fire a global rate limit request to another node.
        
        The remote node will only return when we've grabbed a token or an error occurred.
        """
        if not self.session:
            raise Exception("Session not initialized")
        
        url = f"http://{addr}/nirn/global"
        headers = {
            "bot-hash": str(bot_hash),
            "bot-limit": str(bot_limit)
        }
        
        try:
            async with self.session.get(url, headers=headers) as resp:
                logger.debug("Got go-ahead for global")
                
                if resp.status != 200:
                    raise Exception(f"global request failed with status {resp.status} {resp.reason}")
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Failed to fire global request: {e}")
        except Exception as e:
            raise