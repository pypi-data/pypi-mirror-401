"""Configuration management via environment variables."""
import os
from typing import Optional, List, Dict

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def env_get(name: str, default_val: str) -> str:
    """Get environment variable with default."""
    val = os.getenv(name, "")
    if val == "":
        return default_val
    return val


def env_get_bool(name: str, default_val: bool) -> bool:
    """Get boolean environment variable."""
    val = os.getenv(name, "")
    if val == "":
        return default_val
    
    if val not in ("true", "false"):
        raise ValueError(f"Invalid env var, expected true or false, got {val} for {name}")
    
    return val == "true"


def env_get_int(name: str, default_val: int) -> int:
    """Get integer environment variable."""
    val = os.getenv(name, "")
    if val == "":
        return default_val
    
    try:
        return int(val)
    except ValueError:
        raise ValueError(f"Failed to parse {name}")


class Config:
    """
    Configuration class for nirn.py.
    
    All configuration is loaded from environment variables.
    """
    
    def __init__(self):
        # Logging
        self.log_level = env_get("LOG_LEVEL", "info")
        
        # Server
        self.port = env_get_int("PORT", 8080)
        self.bind_ip = env_get("BIND_IP", "0.0.0.0")
        
        # Metrics
        self.metrics_port = env_get_int("METRICS_PORT", 9000)
        self.enable_metrics = os.getenv("ENABLE_METRICS", "") != "false"
        self.enable_pprof = os.getenv("ENABLE_PPROF", "") == "true"
        
        # Request handling
        self.buffer_size = env_get_int("BUFFER_SIZE", 50)
        self.request_timeout = env_get_int("REQUEST_TIMEOUT", 5000)
        self.max_bearer_count = env_get_int("MAX_BEARER_COUNT", 1024)
        
        # HTTP client
        self.outbound_ip = os.getenv("OUTBOUND_IP") or None
        self.disable_http_2 = env_get_bool("DISABLE_HTTP_2", True)
        
        # Cluster
        self.cluster_port = env_get_int("CLUSTER_PORT", 7946)
        self._cluster_members = os.getenv("CLUSTER_MEMBERS", "")
        self._cluster_dns = os.getenv("CLUSTER_DNS", "")
        
        # Rate limiting
        self._bot_ratelimit_overrides = env_get("BOT_RATELIMIT_OVERRIDES", "")
        self.disable_global_ratelimit_detection = env_get_bool("DISABLE_GLOBAL_RATELIMIT_DETECTION", False)
    
    @property
    def cluster_member_list(self) -> List[str]:
        """Get cluster members list from CLUSTER_MEMBERS."""
        if not self._cluster_members:
            return []
        return [m.strip() for m in self._cluster_members.split(",") if m.strip()]
    
    @property
    def cluster_dns(self) -> Optional[str]:
        """Get cluster DNS from CLUSTER_DNS."""
        return self._cluster_dns if self._cluster_dns else None
    
    @property
    def bot_override_map(self) -> Dict[str, int]:
        """
        Parse bot ratelimit overrides from BOT_RATELIMIT_OVERRIDES.
        
        Format: "<bot_id>:<bot_global_limit>,<bot_id>:<bot_global_limit>"
        """
        if not self._bot_ratelimit_overrides:
            return {}
        
        overrides = {}
        override_list = self._bot_ratelimit_overrides.split(",")
        
        for override in override_list:
            opts = override.split(":")
            if len(opts) != 2:
                raise ValueError("Invalid bot global ratelimit overrides")
            
            try:
                limit = int(opts[1])
            except ValueError:
                raise ValueError("Failed to parse global ratelimit overrides")
            
            overrides[opts[0]] = limit
        
        return overrides