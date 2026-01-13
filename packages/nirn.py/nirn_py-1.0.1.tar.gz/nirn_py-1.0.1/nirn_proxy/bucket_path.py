"""Bucket path utilities for Discord API rate limit handling."""
import base64
from datetime import datetime, timezone, timedelta
from .util import get_snowflake_created_at


# Major resource type constants
MAJOR_UNKNOWN = "unk"
MAJOR_CHANNELS = "channels"
MAJOR_GUILDS = "guilds"
MAJOR_WEBHOOKS = "webhooks"
MAJOR_INVITES = "invites"
MAJOR_INTERACTIONS = "interactions"


def is_snowflake(s: str) -> bool:
    """Check if string is a valid Discord snowflake."""
    length = len(s)
    if length < 17 or length > 20:
        return False
    for char in s:
        if char < '0' or char > '9':
            return False
    return True


def is_numeric_input(s: str) -> bool:
    """Check if string contains only numeric characters."""
    for char in s:
        if char < '0' or char > '9':
            return False
    return True


def get_metrics_path(route: str) -> str:
    """Get sanitized metrics path for Prometheus labels."""
    route = get_optimistic_bucket_path(route, "")
    path = ""
    parts = route.split("/")
    
    if route.startswith("/invite/!"):
        return "/invite/!"
    
    for part in parts:
        if not part:
            continue
        if is_numeric_input(part):
            path += "/!"
        else:
            path += "/" + part
    
    # Ensure valid UTF-8 for Prometheus
    try:
        path.encode('utf-8')
    except UnicodeEncodeError:
        # Replace invalid runes with @
        path = path.encode('utf-8', errors='replace').decode('utf-8').replace('\ufffd', '@')
    
    return path


def get_optimistic_bucket_path(url: str, method: str) -> str:
    """
    Get optimistic bucket path for rate limiting.
    
    This function calculates the bucket path for rate limiting based on the URL and HTTP method.
    """
    bucket = ["/"]
    
    # Split on ? and take first part
    clean_url = url.split("?")[0]
    
    # Handle API version prefix
    if clean_url.startswith("/api/v"):
        # Remove /api/v prefix and find the version number end
        temp = clean_url.replace("/api/v", "", 1)
        idx = temp.find("/")
        if idx != -1:
            clean_url = temp[idx+1:]
        else:
            clean_url = temp
    elif clean_url.startswith("/api/"):
        # Handle unversioned endpoints
        clean_url = clean_url.replace("/api/", "", 1)
    
    parts = clean_url.split("/")
    num_parts = len(parts)
    
    if num_parts <= 1:
        return clean_url
    
    curr_major = MAJOR_UNKNOWN
    
    # Handle major resource types
    if parts[0] == MAJOR_CHANNELS:
        if num_parts == 2:
            # Return the same bucket for all reqs to /channels/id
            return "/channels/!"
        bucket.append(MAJOR_CHANNELS)
        bucket.append("/")
        bucket.append(parts[1])
        curr_major = MAJOR_CHANNELS
        
    elif parts[0] == MAJOR_INVITES:
        bucket.append(MAJOR_INVITES)
        bucket.append("/!")
        curr_major = MAJOR_INVITES
        
    elif parts[0] == MAJOR_GUILDS:
        # guilds/:guildId/channels share the same bucket for all guilds
        if num_parts == 3 and parts[2] == "channels":
            return "/" + MAJOR_GUILDS + "/!/channels"
        # Fallthrough to default
        bucket.append(parts[0])
        bucket.append("/")
        bucket.append(parts[1])
        curr_major = parts[0]
        
    elif parts[0] == MAJOR_INTERACTIONS:
        if num_parts == 4 and parts[3] == "callback":
            return "/" + MAJOR_INTERACTIONS + "/" + parts[1] + "/!/callback"
        # Fallthrough to default
        bucket.append(parts[0])
        bucket.append("/")
        bucket.append(parts[1])
        curr_major = parts[0]
        
    elif parts[0] == MAJOR_WEBHOOKS:
        bucket.append(parts[0])
        bucket.append("/")
        bucket.append(parts[1])
        curr_major = parts[0]
        
    else:
        # Default case
        bucket.append(parts[0])
        bucket.append("/")
        bucket.append(parts[1])
        curr_major = parts[0]
    
    if num_parts == 2:
        return "".join(bucket)
    
    # Process remaining parts (starting from index 2)
    # idx in Go code refers to parts[2:] so we need to track actual index
    for idx, part in enumerate(parts[2:]):
        actual_idx = idx + 2  # Actual index in parts array
        
        if is_snowflake(part):
            # Custom rule for messages older than 14d
            if curr_major == MAJOR_CHANNELS and actual_idx > 0 and parts[actual_idx - 1] == "messages" and method == "DELETE":
                created_at = get_snowflake_created_at(part)
                if created_at:
                    now = datetime.now(timezone.utc)
                    fourteen_days_ago = now - timedelta(days=14)
                    ten_seconds_ago = now - timedelta(seconds=10)
                    
                    if created_at < fourteen_days_ago:
                        bucket.append("/!14dmsg")
                    elif created_at > ten_seconds_ago:
                        bucket.append("/!10smsg")
                continue
            bucket.append("/!")
        else:
            # Handle reactions specially
            if curr_major == MAJOR_CHANNELS and part == "reactions":
                # reaction put/delete fall under a different bucket from other reaction endpoints
                if method == "PUT" or method == "DELETE":
                    bucket.append("/reactions/!modify")
                    break
                # All other reaction endpoints fall under the same bucket
                bucket.append("/reactions/!/!")
                break
            
            # Strip webhook tokens, or extract interaction ID
            if len(part) >= 64:
                # aW50ZXJhY3Rpb246 is base64 for "interaction:"
                if not part.startswith("aW50ZXJhY3Rpb246"):
                    bucket.append("/!")
                    continue
                
                interaction_id = "Unknown"
                
                # Fix padding
                padded = part
                remainder = len(part) % 4
                if remainder != 0:
                    padded += "=" * (4 - remainder)
                
                try:
                    decoded_part = base64.b64decode(padded).decode('utf-8')
                    interaction_id = decoded_part.split(":")[1]
                except Exception:
                    interaction_id = "Unknown"
                
                bucket.append("/")
                bucket.append(interaction_id)
                continue
            
            # Strip webhook tokens and interaction tokens (duplicate check in Go, kept for compatibility)
            if (curr_major == MAJOR_WEBHOOKS or curr_major == MAJOR_INTERACTIONS) and len(part) >= 64:
                bucket.append("/!")
                continue
            
            bucket.append("/")
            bucket.append(part)
    
    return "".join(bucket)


def is_interaction(url: str) -> bool:
    """Check if URL is an interaction endpoint."""
    # Split on ? and take first part
    clean_url = url.split("?")[0]
    parts = clean_url.split("/")
    
    for part in parts:
        if len(part) > 128:
            return True
    
    return False