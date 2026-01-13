"""
nirn.py: Highly available, transparent & dynamic HTTP proxy for Discord API rate limiting.
"""

__version__ = "1.0.0"
__author__ = "Lorenzo"

from .main import main
from .queue_manager import QueueManager
from .config import Config
from .request_queue import RequestQueue, QueueType
from .discord_client import DiscordClient
from .bucket_path import get_optimistic_bucket_path, get_metrics_path, is_interaction
from .util import hash_crc64, has_auth_prefix, get_snowflake_created_at

__all__ = [
    "main",
    "QueueManager", 
    "Config",
    "RequestQueue",
    "QueueType",
    "DiscordClient",
    "get_optimistic_bucket_path",
    "get_metrics_path",
    "is_interaction",
    "hash_crc64",
    "has_auth_prefix",
    "get_snowflake_created_at",
]