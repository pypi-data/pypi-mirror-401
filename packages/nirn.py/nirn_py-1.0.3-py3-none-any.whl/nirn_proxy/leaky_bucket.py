"""Leaky bucket rate limiter implementation."""
import asyncio
import time
from typing import Dict


class LeakyBucket:
    """
    Leaky bucket rate limiter.
    
    The bucket allows `capacity` tokens per `period` seconds.
    When Add() is called, it checks if there's capacity available.
    """
    
    def __init__(self, name: str, capacity: int, period: float):
        self.name = name
        self.capacity = capacity
        self.period = period  # seconds
        self.tokens = 0
        self.last_update = time.time()
        self._lock = asyncio.Lock()
    
    def _leak(self) -> None:
        """Leak tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_update
        
        # Calculate how many tokens have leaked
        leaked = int(elapsed / self.period * self.capacity)
        if leaked > 0:
            self.tokens = max(0, self.tokens - leaked)
            self.last_update = now
    
    async def add(self, count: int = 1) -> bool:
        """
        Try to add tokens to the bucket.
        Returns True if successful (within capacity), False if bucket is full.
        """
        async with self._lock:
            self._leak()
            
            if self.tokens + count <= self.capacity:
                self.tokens += count
                return True
            return False
    
    def reset_time(self) -> float:
        """Get the time when the bucket will reset (have capacity available)."""
        # Calculate when tokens will leak enough to allow new requests
        tokens_to_leak = self.tokens - self.capacity + 1
        if tokens_to_leak <= 0:
            return time.time()
        
        time_to_leak = (tokens_to_leak / self.capacity) * self.period
        return self.last_update + time_to_leak


class BucketManager:
    """
    Manages multiple leaky buckets.
    """
    
    def __init__(self):
        self.buckets: Dict[str, LeakyBucket] = {}
        self._lock = asyncio.Lock()
    
    async def create(self, name: str, capacity: int, period: float) -> LeakyBucket:
        """Create a new bucket."""
        async with self._lock:
            bucket = LeakyBucket(name, capacity, period)
            self.buckets[name] = bucket
            return bucket
    
    async def get_or_create(self, name: str, capacity: int, period: float) -> LeakyBucket:
        """Get existing bucket or create a new one."""
        async with self._lock:
            if name not in self.buckets:
                self.buckets[name] = LeakyBucket(name, capacity, period)
            return self.buckets[name]
    
    async def take(self, name: str, capacity: int, period: float) -> None:
        """
        Take a token from the bucket, waiting if necessary.
        
        Matches the Go pattern:
        takeGlobal:
            _, err := bucket.Add(1)
            if err != nil {
                reset := bucket.Reset()
                time.Sleep(time.Until(reset))
                goto takeGlobal
            }
        """
        bucket = await self.get_or_create(name, capacity, period)
        
        while True:
            success = await bucket.add(1)
            if success:
                return
            
            # Wait until bucket resets
            reset_time = bucket.reset_time()
            wait_time = reset_time - time.time()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
