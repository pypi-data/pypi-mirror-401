"""Utility functions for hashing, snowflakes, and helpers."""
import base64
import time
import socket
from typing import Optional
from datetime import datetime, timezone


# CRC64-ISO polynomial and table
_CRC64_ISO_POLY = 0xD800000000000000


def _make_crc64_table():
    """Generate CRC64-ISO lookup table."""
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ _CRC64_ISO_POLY
            else:
                crc >>= 1
        table.append(crc)
    return table


_CRC64_TABLE = _make_crc64_table()


def hash_crc64(data: str) -> int:
    """CRC64-ISO hash function."""
    crc = 0
    for byte in data.encode('utf-8'):
        crc = _CRC64_TABLE[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    return crc


# Discord epoch constant
EPOCH_DISCORD = 1420070400000


def get_snowflake_created_at(snowflake: str) -> Optional[datetime]:
    """Get creation time from Discord snowflake."""
    try:
        parsed_id = int(snowflake)
        epoch = (parsed_id >> 22) + EPOCH_DISCORD
        return datetime.fromtimestamp(epoch / 1000, tz=timezone.utc)
    except (ValueError, OSError):
        return datetime.now(timezone.utc)


def get_bot_id(token: str) -> str:
    """Extract bot ID from token."""
    if not token:
        return "NoAuth"
    
    # Remove auth prefixes
    token = token.replace("Bot ", "").replace("Bearer ", "").replace("Basic ", "")
    
    # Get first part before dot
    token_part = token.split(".")[0]
    
    try:
        decoded = base64.b64decode(token_part)
        return decoded.decode('utf-8')
    except Exception:
        return "Unknown"


def has_auth_prefix(token: str, scheme: str) -> bool:
    """
    Check if the provided authorization header value starts with the given scheme.
    Comparison is performed case-insensitively and requires the scheme to be 
    followed by at least one space as mandated by RFC 7235.
    
    Matches Go implementation exactly.
    """
    if len(token) <= len(scheme):
        return False
    
    if token[:len(scheme)].lower() != scheme.lower():
        return False
    
    # Check if followed by space or tab
    next_char = token[len(scheme)]
    return next_char in (' ', '\t')


def get_local_ip() -> str:
    """Get local IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def generate_node_name() -> str:
    """Generate unique node name."""
    hostname = socket.gethostname()
    timestamp = int(time.time() * 1000)
    return f"{hostname}-{timestamp}"