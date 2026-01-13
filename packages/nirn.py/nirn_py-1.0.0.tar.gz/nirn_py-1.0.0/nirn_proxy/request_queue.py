"""Request queue for handling per-route Discord rate limits."""
import asyncio
import os
import time
import logging
from typing import Optional, Dict, Any, TYPE_CHECKING
from asyncio import Queue
from dataclasses import dataclass
from enum import IntEnum
from .bucket_path import get_optimistic_bucket_path, is_interaction
from .leaky_bucket import BucketManager
from .util import has_auth_prefix

if TYPE_CHECKING:
    from .discord_client import DiscordClient, DiscordResponse


logger = logging.getLogger(__name__)


class QueueType(IntEnum):
    """Queue type enumeration."""
    BOT = 0
    NO_AUTH = 1
    BEARER = 2


@dataclass
class QueueItem:
    """Queue item containing request data and response futures."""
    method: str
    path: str
    headers: Dict[str, str]
    body: Optional[bytes]
    query: str
    done_future: asyncio.Future  # doneChan equivalent
    err_future: asyncio.Future   # errChan equivalent


@dataclass
class QueueChannel:
    """Queue channel with async queue and last used timestamp."""
    ch: Queue
    last_used: float


@dataclass 
class BotUserResponse:
    """Bot user response containing ID, username, and discriminator."""
    id: str
    username: str
    discrim: str


class RequestQueue:
    """
    Request queue for handling Discord rate limits.
    
    Key behaviors:
    - One async task per bucket path (subscribe function)
    - Global rate limit handling with atomic operations
    - Fail-fast for webhook 404s
    - 401 token invalidation
    - Sweep unused queues every 5 minutes
    """
    
    def __init__(
        self,
        processor: callable,
        token: str,
        buffer_size: int,
        global_limit: int,
        queue_type: QueueType,
        user: Optional[BotUserResponse] = None,
        identifier: str = "NoAuth"
    ):
        self.processor = processor
        self.buffer_size = buffer_size
        self.bot_limit = global_limit
        self.queue_type = queue_type
        self.user = user
        self.identifier = identifier
        
        # Bucket queues: path_hash -> QueueChannel
        self.queues: Dict[int, QueueChannel] = {}
        self._queues_lock = asyncio.Lock()
        
        # Global rate limiting
        self.global_locked_until = 0
        
        # Global bucket
        self.global_bucket_manager = BucketManager()
        
        # Token validation
        self.is_token_invalid = 0
        
        # Destroyed flag
        self._destroyed = False
        
        # Start sweep task for non-bearer queues
        if queue_type != QueueType.BEARER:
            logger.info(f"Created new queue - globalLimit: {global_limit}, identifier: {identifier}, bufferSize: {buffer_size}")
            asyncio.create_task(self._tick_sweep())
        else:
            logger.debug(f"Created new bearer queue - globalLimit: {global_limit}, identifier: {identifier}, bufferSize: {buffer_size}")
    
    async def destroy(self):
        """Destroy the queue and signal all subscribers to stop."""
        async with self._queues_lock:
            logger.debug("Destroying queue")
            self._destroyed = True
            for queue_channel in self.queues.values():
                # Signal shutdown by putting None (close channel equivalent)
                try:
                    queue_channel.ch.put_nowait(None)
                except asyncio.QueueFull:
                    pass
    
    async def _sweep(self):
        """Sweep unused bucket queues (older than 10 minutes)."""
        async with self._queues_lock:
            logger.info("Sweep start")
            swept_entries = 0
            current_time = time.time()
            keys_to_remove = []
            
            for path_hash, queue_channel in self.queues.items():
                if current_time - queue_channel.last_used > 600:  # 10 minutes
                    keys_to_remove.append(path_hash)
            
            for key in keys_to_remove:
                queue_channel = self.queues[key]
                try:
                    queue_channel.ch.put_nowait(None)
                except asyncio.QueueFull:
                    pass
                del self.queues[key]
                swept_entries += 1
            
            logger.info(f"Finished sweep - sweptEntries: {swept_entries}")
    
    async def _tick_sweep(self):
        """Sweep unused queues every 5 minutes."""
        while not self._destroyed:
            await asyncio.sleep(300)  # 5 minutes
            if not self._destroyed:
                await self._sweep()
    
    async def queue(self, req_method: str, req_path: str, req_headers: Dict[str, str],
                   req_body: Optional[bytes], req_query: str, path: str, path_hash: int) -> Any:
        """
        Queue a request for rate-limited processing.
        
        Returns the response or raises an error.
        """
        logger.debug(f"Inbound request - bucket: {path}, path: {req_path}, method: {req_method}")
        
        queue_channel = await self._get_queue_channel(path, path_hash)
        
        loop = asyncio.get_running_loop()
        done_future = loop.create_future()
        err_future = loop.create_future()
        
        item = QueueItem(
            method=req_method,
            path=req_path,
            headers=req_headers,
            body=req_body,
            query=req_query,
            done_future=done_future,
            err_future=err_future
        )
        
        # safeSend equivalent - handle closed queue gracefully
        try:
            queue_channel.ch.put_nowait(item)
        except asyncio.QueueFull:
            err_future.set_exception(Exception("failed to send due to closed channel, sending 429 for client to retry"))
            raise Exception("Queue full - 429")
        
        # Wait for either done or error
        done_task = asyncio.create_task(self._wait_future(done_future))
        err_task = asyncio.create_task(self._wait_future(err_future))
        
        done, pending = await asyncio.wait(
            [done_task, err_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        for task in pending:
            task.cancel()
        
        # Check which completed
        if done_future.done() and not done_future.cancelled():
            try:
                return done_future.result()
            except Exception:
                pass
        
        if err_future.done() and not err_future.cancelled():
            try:
                raise err_future.result()
            except Exception as e:
                raise e
        
        # Return from done future
        return await done_task
    
    async def _wait_future(self, future: asyncio.Future):
        """Wait for a future to complete."""
        return await future
    
    async def _get_queue_channel(self, path: str, path_hash: int) -> QueueChannel:
        """Get or create queue channel for a bucket path."""
        t = time.time()
        
        async with self._queues_lock:
            if path_hash in self.queues:
                self.queues[path_hash].last_used = t
                return self.queues[path_hash]
            
            # Create new queue channel
            queue_channel = QueueChannel(
                ch=Queue(maxsize=self.buffer_size),
                last_used=t
            )
            self.queues[path_hash] = queue_channel
            
            # Start subscriber task
            asyncio.create_task(self._subscribe(queue_channel, path, path_hash))
            
            return queue_channel
    
    async def _subscribe(self, ch: QueueChannel, path: str, path_hash: int):
        """
        Process bucket queue for rate limit handling.
        
        This is the core rate limit handling logic - one async task per bucket.
        """
        prev_rem = 0
        prev_reset = 0.0
        ret_404 = False
        
        while True:
            try:
                item: Optional[QueueItem] = await ch.ch.get()
                
                # Check for shutdown signal
                if item is None:
                    break
                
                # Fail fast for webhook 404s
                if ret_404:
                    self._return_404_webhook(item)
                    continue
                
                # Check for invalid token
                if self.is_token_invalid > 0:
                    self._return_401(item)
                    continue
                
                # Process the request
                try:
                    resp = await self.processor(item, self.identifier)
                    
                    scope = resp.headers.get("x-ratelimit-scope", "")
                    
                    _, remaining, reset_after, is_global = self._parse_headers(resp.headers, scope != "user")
                    
                    # Handle global rate limit
                    if is_global:
                        # Atomic compare and swap equivalent
                        if self.global_locked_until == 0:
                            new_lock_time = time.time() + reset_after
                            self.global_locked_until = new_lock_time
                            logger.warning(f"Global reached, locking - until: {new_lock_time}, resetAfter: {reset_after}")
                    
                    # Send response to waiting caller
                    if not item.done_future.done():
                        item.done_future.set_result(resp)
                    
                    # Log unexpected 429s
                    if resp.status == 429 and scope != "shared":
                        logger.warning(
                            f"Unexpected 429 - prevRemaining: {prev_rem}, prevResetAfter: {prev_reset}, "
                            f"remaining: {remaining}, resetAfter: {reset_after}, bucket: {path}, "
                            f"route: {item.path}, method: {item.method}, isGlobal: {is_global}, "
                            f"pathHash: {path_hash}, discordBucket: {resp.headers.get('x-ratelimit-bucket')}, "
                            f"ratelimitScope: {scope}"
                        )
                    
                    # Handle webhook 404 fail-fast
                    if resp.status == 404 and path.startswith("/webhooks/") and not is_interaction(item.path):
                        logger.info(f"Setting fail fast 404 for webhook - bucket: {path}, route: {item.path}, method: {item.method}")
                        ret_404 = True
                    
                    # Handle 401 token invalidation
                    if resp.status == 401 and not is_interaction(item.path) and self.queue_type != QueueType.NO_AUTH:
                        logger.error(
                            f"Received 401 during normal operation, assuming token is invalidated, "
                            f"locking bucket permanently - bucket: {path}, route: {item.path}, "
                            f"method: {item.method}, identifier: {self.identifier}, status: {resp.status}"
                        )
                        
                        if os.getenv("DISABLE_401_LOCK", "false") != "true":
                            self.is_token_invalid = 999
                    
                    # Prevent reaction bucket from being stuck
                    if (resp.status == 429 and scope == "shared" and 
                        path in ("/channels/!/messages/!/reactions/!modify", "/channels/!/messages/!/reactions/!/!")):
                        prev_rem = remaining
                        prev_reset = reset_after
                        continue
                    
                    # Wait for rate limit reset
                    if remaining == 0 or resp.status == 429:
                        if reset_after > 0:
                            await asyncio.sleep(reset_after)
                    
                    prev_rem = remaining
                    prev_reset = reset_after
                    
                except Exception as e:
                    if not item.err_future.done():
                        item.err_future.set_exception(e)
                    
            except Exception as e:
                logger.error(f"Error in subscribe loop for {path}: {e}")
    
    def _parse_headers(self, headers: Dict[str, str], prefer_retry_after: bool) -> tuple:
        """
        Parse rate limit headers from Discord response.
        
        Returns: (limit, remaining, reset_after, is_global)
        """
        if headers is None:
            return 0, 0, 0.0, False
        
        limit_str = headers.get("x-ratelimit-limit", "")
        remaining_str = headers.get("x-ratelimit-remaining", "")
        reset_after_str = headers.get("x-ratelimit-reset-after", "")
        retry_after_str = headers.get("retry-after", "")
        
        # Use retry-after for globals or shared ratelimits
        if not reset_after_str or (prefer_retry_after and retry_after_str):
            reset_after_str = retry_after_str
        
        is_global = headers.get("x-ratelimit-global") == "true"
        
        reset_after = 0.0
        if reset_after_str:
            try:
                reset_after = float(reset_after_str)
            except ValueError:
                pass
        
        if is_global:
            return 0, 0, reset_after, True
        
        if not limit_str:
            return 0, 0, reset_after, False
        
        try:
            limit = int(limit_str)
            remaining = int(remaining_str) if remaining_str else 0
            return limit, remaining, reset_after, is_global
        except ValueError:
            return 0, 0, reset_after, False
    
    def _return_404_webhook(self, item: QueueItem):
        """Return 404 response for invalid webhook."""
        from .discord_client import DiscordResponse
        
        resp = DiscordResponse(
            status=404,
            status_text="Not Found",
            headers={"content-type": "application/json"},
            body=b'{\n  "message": "Unknown Webhook",\n  "code": 10015\n}'
        )
        
        if not item.done_future.done():
            item.done_future.set_result(resp)
    
    def _return_401(self, item: QueueItem):
        """Return 401 response for invalid token."""
        from .discord_client import DiscordResponse
        
        resp = DiscordResponse(
            status=401,
            status_text="Unauthorized",
            headers={"content-type": "application/json"},
            body=b'{\n\t"message": "401: Unauthorized",\n\t"code": 0\n}'
        )
        
        if not item.done_future.done():
            item.done_future.set_result(resp)