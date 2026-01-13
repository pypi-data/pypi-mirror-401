"""Queue manager for handling Discord API rate limiting and request routing."""
import asyncio
import logging
import time
import os
from typing import Dict, Optional, Tuple, List, Any
from cachetools import LRUCache
from aiohttp import web
from .config import Config
from .request_queue import RequestQueue, QueueType, QueueItem, BotUserResponse
from .discord_client import DiscordClient, DiscordResponse
from .bucket_path import get_optimistic_bucket_path, get_metrics_path
from .metrics import open_connections, error_counter, requests_routed_sent, requests_routed_received, requests_routed_error
from .memberlist import Memberlist, MemberlistDelegate, Node
from .distributed_global import ClusterGlobalRateLimiter
from .util import hash_crc64, has_auth_prefix


logger = logging.getLogger(__name__)


# Paths that should be routed locally to avoid cluster bottlenecks
PATHS_TO_ROUTE_LOCALLY = {
    hash_crc64("/users/@me/channels"),
    hash_crc64("/users/@me")
}


def _on_evict_lru_item(key: str, value: RequestQueue):
    """Callback when bearer queue is evicted from LRU cache."""
    asyncio.create_task(value.destroy())


class QueueManager:
    """
    Queue manager for Discord API rate limiting.
    
    Handles:
    - Bot queues (persistent map)
    - Bearer queues (LRU cache)
    - Cluster routing
    - Global rate limiting across cluster
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.discord_client: Optional[DiscordClient] = None
        
        # Bot queues
        self.queues: Dict[str, RequestQueue] = {}
        self._queues_lock = asyncio.Lock()
        
        # Bearer queues with LRU eviction
        self.bearer_queues: Dict[str, RequestQueue] = {}
        self._bearer_queues_lock = asyncio.Lock()
        self._bearer_lru_order: List[str] = []
        self._max_bearer_count = config.max_bearer_count
        
        # Cluster support
        self.cluster: Optional[Memberlist] = None
        self.cluster_global_rate_limiter = ClusterGlobalRateLimiter()
        self.ordered_cluster_members: List[str] = []
        self.name_to_address_map: Dict[str, str] = {}
        self.local_node_name = ""
        self.local_node_ip = ""
        self.local_node_proxy_listen_addr = ""
    
    async def initialize(self):
        """Initialize the queue manager."""
        self.discord_client = DiscordClient(self.config)
        await self.discord_client.__aenter__()
        await self.cluster_global_rate_limiter.__aenter__()
        
        # Initialize cluster if configured
        if self.config.cluster_member_list or self.config.cluster_dns:
            await self._init_cluster()
    
    async def shutdown(self):
        """Shutdown the queue manager and clean up resources."""
        if self.cluster:
            await self.cluster.stop(30.0)
        
        # Destroy all queues
        for queue in self.queues.values():
            await queue.destroy()
        
        for queue in self.bearer_queues.values():
            await queue.destroy()
        
        await self.cluster_global_rate_limiter.__aexit__(None, None, None)
        
        if self.discord_client:
            await self.discord_client.__aexit__(None, None, None)
    
    async def _init_cluster(self):
        """Initialize cluster membership."""
        delegate = MemberlistDelegate()
        delegate.on_join = self._on_node_join
        delegate.on_leave = self._on_node_leave
        
        self.cluster = Memberlist(
            bind_port=self.config.cluster_port,
            proxy_port=str(self.config.port),
            delegate=delegate
        )
        
        # Determine existing members
        existing_members = []
        if self.config.cluster_member_list:
            existing_members = [f"{member}:{self.config.cluster_port}" 
                              for member in self.config.cluster_member_list]
        elif self.config.cluster_dns:
            try:
                import socket
                ips = socket.gethostbyname_ex(self.config.cluster_dns)[2]
                existing_members = [f"{ip}:{self.config.cluster_port}" for ip in ips]
            except Exception as e:
                logger.error(f"Failed to resolve cluster DNS: {e}")
        
        await self.cluster.start(existing_members)
        
        # Set local node info
        self.local_node_name = self.cluster.local_node.name
        self.local_node_ip = self.cluster.local_node.addr
        self.local_node_proxy_listen_addr = f"{self.local_node_ip}:{self.config.port}"
        
        self._reindex_members()
    
    def _on_node_join(self, node: Node):
        """Handle node join - run in async task to prevent deadlock."""
        asyncio.create_task(self._reindex_members_async())
    
    def _on_node_leave(self, node: Node):
        """Handle node leave - run in async task to prevent deadlock."""
        asyncio.create_task(self._reindex_members_async())
    
    async def _reindex_members_async(self):
        """Async wrapper for reindex."""
        self._reindex_members()
    
    def _reindex_members(self):
        """Reindex cluster members and update routing tables."""
        if not self.cluster:
            logger.warning("reindexMembers called but cluster is nil")
            return
        
        members = self.cluster.get_members()
        ordered_members = []
        name_to_address_map = {}
        
        for member in members:
            ordered_members.append(member.name)
            proxy_port = member.meta.decode() if member.meta else str(self.config.port)
            name_to_address_map[member.name] = f"{member.addr}:{proxy_port}"
        
        ordered_members.sort()
        
        self.ordered_cluster_members = ordered_members
        self.name_to_address_map = name_to_address_map
    
    def _calculate_route(self, path_hash: int) -> str:
        """Calculate which cluster node should handle this request."""
        if not self.cluster:
            return ""
        
        if path_hash == 0:
            return ""
        
        if path_hash in PATHS_TO_ROUTE_LOCALLY:
            return ""
        
        members = self.ordered_cluster_members
        count = len(members)
        
        if count == 0:
            return ""
        
        chosen_index = path_hash % count
        addr = self.name_to_address_map.get(members[chosen_index], "")
        
        if addr == self.local_node_proxy_listen_addr:
            return ""
        
        return addr
    
    async def _route_request(self, addr: str, request: web.Request) -> web.Response:
        """Route request to another cluster node."""
        url = f"http://{addr}{request.path}"
        if request.query_string:
            url += f"?{request.query_string}"
        
        headers = dict(request.headers)
        headers["nirn-routed-to"] = addr
        
        body = await request.read() if request.can_read_body else None
        
        logger.debug(f"Routing request to node in cluster - to: {addr}, path: {request.path}, method: {request.method}")
        
        try:
            async with self.discord_client.session.request(
                request.method, url, headers=headers, data=body
            ) as resp:
                logger.debug(f"Received response from node - to: {addr}, path: {request.path}, method: {request.method}")
                requests_routed_sent.inc()
                
                response_body = await resp.read()
                response_headers = dict(resp.headers)
                
                return web.Response(
                    body=response_body,
                    status=resp.status,
                    headers=response_headers
                )
        except Exception as e:
            requests_routed_error.inc()
            logger.error(f"Failed to route request: {e}")
            return self._generate_429_response()
    
    def _get_request_routing_info(self, request: web.Request, token: str) -> Tuple[int, str, QueueType]:
        """Get routing info for a request."""
        path = get_optimistic_bucket_path(request.path, request.method)
        queue_type = QueueType.NO_AUTH
        routing_hash = hash_crc64(path)
        
        if has_auth_prefix(token, "Bearer"):
            queue_type = QueueType.BEARER
            routing_hash = hash_crc64(token)
        elif token and not has_auth_prefix(token, "Basic"):
            queue_type = QueueType.BOT
        
        return routing_hash, path, queue_type
    
    async def _get_or_create_bot_queue(self, token: str) -> RequestQueue:
        """Get or create a queue for a bot token."""
        # Check with read lock first
        if token in self.queues:
            return self.queues[token]
        
        async with self._queues_lock:
            # Double-check after acquiring lock
            if token in self.queues:
                return self.queues[token]
            
            # Create new queue
            queue = await self._create_request_queue(token)
            self.queues[token] = queue
            return queue
    
    async def _get_or_create_bearer_queue(self, token: str) -> RequestQueue:
        """Get or create a queue for a bearer token (with LRU eviction)."""
        async with self._bearer_queues_lock:
            if token in self.bearer_queues:
                # Update LRU order
                if token in self._bearer_lru_order:
                    self._bearer_lru_order.remove(token)
                self._bearer_lru_order.append(token)
                return self.bearer_queues[token]
            # Double-check after acquiring lock
            if token in self.bearer_queues:
                if token in self._bearer_lru_order:
                    self._bearer_lru_order.remove(token)
                self._bearer_lru_order.append(token)
                return self.bearer_queues[token]
            
            # Evict oldest if at capacity
            while len(self.bearer_queues) >= self._max_bearer_count and self._bearer_lru_order:
                oldest_key = self._bearer_lru_order.pop(0)
                if oldest_key in self.bearer_queues:
                    old_queue = self.bearer_queues.pop(oldest_key)
                    asyncio.create_task(old_queue.destroy())
            
            # Create new bearer queue with buffer size 5
            async def bearer_processor(item: QueueItem, identifier: str) -> DiscordResponse:
                return await self.discord_client.make_request(
                    item.method, item.path, item.headers, item.body, item.query, identifier
                )
            
            queue = RequestQueue(
                processor=bearer_processor,
                token=token,
                buffer_size=5,  # Bearer queues have smaller buffer
                global_limit=50,
                queue_type=QueueType.BEARER,
                user=None,
                identifier="Bearer"
            )
            
            self.bearer_queues[token] = queue
            self._bearer_lru_order.append(token)
            
            return queue
    
    async def _create_request_queue(self, token: str) -> RequestQueue:
        """Create a new request queue for a token."""
        queue_type = QueueType.NO_AUTH
        user: Optional[BotUserResponse] = None
        
        # Determine queue type
        if has_auth_prefix(token, "Bearer"):
            queue_type = QueueType.BEARER
        elif token and not has_auth_prefix(token, "Basic"):
            # Try to get bot user info
            try:
                user_data = await self.discord_client.get_bot_user(token)
                if user_data:
                    user = BotUserResponse(
                        id=user_data.get("id", ""),
                        username=user_data.get("username", ""),
                        discrim=user_data.get("discriminator", "")
                    )
            except Exception as e:
                pass
        
        # Get global limit
        try:
            gateway_data = None
            if token and not has_auth_prefix(token, "Bearer") and not has_auth_prefix(token, "Basic"):
                try:
                    gateway_data = await self.discord_client.get_bot_gateway(token)
                except Exception as e:
                    if "invalid token" in str(e):
                        # Return a queue that will only return 401s
                        async def invalid_processor(item: QueueItem, identifier: str) -> DiscordResponse:
                            return await self.discord_client.make_request(
                                item.method, item.path, item.headers, item.body, item.query, identifier
                            )
                        
                        queue = RequestQueue(
                            processor=invalid_processor,
                            token=token,
                            buffer_size=self.config.buffer_size,
                            global_limit=2**31 - 1,
                            queue_type=QueueType.BOT,
                            user=None,
                            identifier="InvalidTokenQueue"
                        )
                        queue.is_token_invalid = 999
                        return queue
                    raise
            
            global_limit = self.discord_client.get_bot_global_limit(
                token, 
                {"id": user.id} if user else None, 
                gateway_data
            )
        except Exception as e:
            if "invalid token" in str(e):
                async def invalid_processor(item: QueueItem, identifier: str) -> DiscordResponse:
                    return await self.discord_client.make_request(
                        item.method, item.path, item.headers, item.body, item.query, identifier
                    )
                
                queue = RequestQueue(
                    processor=invalid_processor,
                    token=token,
                    buffer_size=self.config.buffer_size,
                    global_limit=2**31 - 1,
                    queue_type=QueueType.BOT,
                    user=None,
                    identifier="InvalidTokenQueue"
                )
                queue.is_token_invalid = 999
                return queue
            raise
        
        # Determine identifier
        identifier = "NoAuth"
        if user:
            queue_type = QueueType.BOT
            identifier = f"{user.username}#{user.discrim}"
        
        if queue_type == QueueType.BEARER:
            identifier = "Bearer"
        
        # Create processor function
        async def processor(item: QueueItem, identifier: str) -> DiscordResponse:
            return await self.discord_client.make_request(
                item.method, item.path, item.headers, item.body, item.query, identifier
            )
        
        return RequestQueue(
            processor=processor,
            token=token,
            buffer_size=self.config.buffer_size,
            global_limit=global_limit,
            queue_type=queue_type,
            user=user,
            identifier=identifier
        )
    
    async def discord_request_handler(self, request: web.Request) -> web.Response:
        """Handle incoming Discord API requests."""
        req_start = time.time()
        metrics_path = get_metrics_path(request.path)
        
        open_connections.labels(route=metrics_path, method=request.method).inc()
        
        try:
            token = request.headers.get("Authorization", "")
            routing_hash, path, queue_type = self._get_request_routing_info(request, token)
            
            return await self._fulfill_request(
                request, queue_type, path, routing_hash, token, req_start
            )
        finally:
            open_connections.labels(route=metrics_path, method=request.method).dec()
    
    async def _fulfill_request(
        self, 
        request: web.Request,
        queue_type: QueueType,
        path: str,
        path_hash: int,
        token: str,
        req_start: float
    ) -> web.Response:
        """Fulfill the incoming request using the appropriate queue."""
        log_fields = {"clientIp": request.remote}
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            log_fields["forwardedFor"] = forwarded_for
        
        route_to = self._calculate_route(path_hash)
        route_to_header = request.headers.get("nirn-routed-to", "")
        
        if route_to_header:
            requests_routed_received.inc()
        
        if route_to and not route_to_header:
            # Route to another node
            try:
                return await self._route_request(route_to, request)
            except Exception as e:
                logger.error(f"routeRequest failed: {e}")
                return self._generate_429_response()
        
        # Handle locally
        try:
            if queue_type == QueueType.BEARER:
                q = await self._get_or_create_bearer_queue(token)
            else:
                q = await self._get_or_create_bot_queue(token)
        except Exception as e:
            if "429" in str(e):
                self._generate_429_response()
                logger.warning(f"getOrCreateQueue failed: {e}")
            else:
                error_counter.inc()
                logger.error(f"getOrCreateQueue failed: {e}")
                return web.Response(text=str(e), status=500)
            return self._generate_429_response()
        
        # Handle global rate limiting for authenticated requests
        if q.identifier != "NoAuth":
            bot_hash = 0
            if q.user:
                bot_hash = hash_crc64(q.user.id)
            
            bot_limit = q.bot_limit
            global_route_to = self._calculate_route(bot_hash)
            
            if not global_route_to or queue_type == QueueType.BEARER:
                await self.cluster_global_rate_limiter.take(bot_hash, bot_limit)
            else:
                try:
                    await self.cluster_global_rate_limiter.fire_global_request(
                        global_route_to, bot_hash, bot_limit
                    )
                except Exception as e:
                    logger.error(f"FireGlobalRequest failed: {e}")
                    error_counter.inc()
                    return self._generate_429_response()
        
        # Read request body
        body = await request.read() if request.can_read_body else None
        
        # Queue the request
        try:
            response = await q.queue(
                req_method=request.method,
                req_path=request.path,
                req_headers=dict(request.headers),
                req_body=body,
                req_query=request.query_string,
                path=path,
                path_hash=path_hash
            )
            
            return await self._convert_response(response)
            
        except Exception as e:
            import asyncio
            if isinstance(e, asyncio.TimeoutError):
                logger.warning(f"Queue timeout - waitedFor: {time.time() - req_start}")
            elif "context" in str(e).lower() or "cancel" in str(e).lower():
                logger.warning(f"Queue cancelled: {e}")
            else:
                logger.error(f"Queue error: {e}")
            
            return self._generate_429_response()
    
    async def _convert_response(self, discord_response: DiscordResponse) -> web.Response:
        """Convert Discord response to web response."""
        # Copy headers
        headers = {}
        for key, value in discord_response.headers.items():
            if key.lower() != "content-length":
                headers[key.lower()] = value
        
        return web.Response(
            body=discord_response.body,
            status=discord_response.status,
            headers=headers
        )
    
    def _generate_429_response(self) -> web.Response:
        """Generate a 429 rate limit response."""
        import time
        
        headers = {
            "generated-by-proxy": "true",
            "x-ratelimit-scope": "user",
            "x-ratelimit-limit": "1",
            "x-ratelimit-remaining": "0",
            "x-ratelimit-reset": str(int(time.time()) + 1),
            "x-ratelimit-after": "1",
            "retry-after": "1",
            "content-type": "application/json"
        }
        
        body = '{\n\t"global": false,\n\t"message": "You are being rate limited.",\n\t"retry_after": 1\n}'
        
        return web.Response(
            body=body.encode(),
            status=429,
            headers=headers
        )
    
    async def handle_global(self, request: web.Request) -> web.Response:
        """Handle global rate limit coordination requests from other nodes."""
        bot_hash_str = request.headers.get("bot-hash")
        bot_limit_str = request.headers.get("bot-limit")
        
        if not bot_hash_str or not bot_limit_str:
            return web.Response(status=400)
        
        try:
            bot_hash = int(bot_hash_str)
            bot_limit = int(bot_limit_str)
        except ValueError:
            return web.Response(status=400)
        
        await self.cluster_global_rate_limiter.take(bot_hash, bot_limit)
        logger.debug("Returned OK for global request")
        
        return web.Response(status=200)
    
    async def handle_healthz(self, request: web.Request) -> web.Response:
        """Handle health check requests."""
        return web.Response(status=200)
    
    def create_app(self) -> web.Application:
        """Create the aiohttp web application."""
        app = web.Application()
        
        # Register routes
        app.router.add_route("*", "/nirn/global", self.handle_global)
        app.router.add_route("*", "/nirn/healthz", self.handle_healthz)
        app.router.add_route("*", "/{path:.*}", self.discord_request_handler)
        
        return app