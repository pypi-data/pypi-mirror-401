"""Utility helpers for LLMCacheX."""

import time
import hashlib
import json
from typing import Any, Dict, Optional
from datetime import datetime, timedelta


def now() -> int:
    """Get current Unix timestamp."""
    return int(time.time())


def now_iso() -> str:
    """Get current ISO 8601 timestamp."""
    return datetime.utcnow().isoformat() + "Z"


def timestamp_to_datetime(ts: int) -> datetime:
    """Convert Unix timestamp to datetime."""
    return datetime.utcfromtimestamp(ts)


def parse_duration(duration: str) -> int:
    """Parse duration string to seconds.

    Examples:
        "30s" -> 30
        "5m" -> 300
        "1h" -> 3600
        "1d" -> 86400
    """
    if not duration:
        return 0

    duration = duration.strip().lower()
    multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800,
    }

    for unit, multiplier in multipliers.items():
        if duration.endswith(unit):
            try:
                value = float(duration[:-1])
                return int(value * multiplier)
            except ValueError:
                return 0

    return 0


def bytes_to_mb(bytes_val: int) -> float:
    """Convert bytes to megabytes."""
    return bytes_val / (1024 * 1024)


def mb_to_bytes(mb_val: float) -> int:
    """Convert megabytes to bytes."""
    return int(mb_val * 1024 * 1024)


def format_size(bytes_val: int) -> str:
    """Format bytes as human-readable size.

    Examples:
        1024 -> "1.0 KB"
        1048576 -> "1.0 MB"
        1073741824 -> "1.0 GB"
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"


def format_cost(cost: float) -> str:
    """Format cost as currency string.

    Examples:
        0.0024 -> "$0.0024"
        1.5 -> "$1.50"
    """
    return f"${cost:.4f}".rstrip('0').rstrip('.')


def similarity_to_percentage(similarity: float) -> str:
    """Convert similarity score (0-1) to percentage.

    Examples:
        0.92 -> "92%"
        0.9234 -> "92%"
    """
    return f"{similarity * 100:.0f}%"


def safe_json_serialize(obj: Any) -> Optional[str]:
    """Safely serialize object to JSON, handling non-serializable types."""
    try:
        return json.dumps(obj, default=str)
    except (TypeError, ValueError):
        return None


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to max length with suffix.

    Examples:
        ("hello world", 5) -> "he..."
        ("short", 10) -> "short"
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_key(key: str) -> str:
    """Sanitize cache key by removing unsafe characters."""
    import re
    # Keep alphanumeric, hyphen, underscore
    return re.sub(r'[^a-zA-Z0-9-_]', '_', key)


def validate_threshold(threshold: float) -> bool:
    """Validate semantic similarity threshold."""
    return 0.0 <= threshold <= 1.0


def validate_temperature(temperature: float) -> bool:
    """Validate LLM temperature parameter."""
    return 0.0 <= temperature <= 2.0


def calculate_expiry(ttl_seconds: int) -> int:
    """Calculate expiry timestamp from TTL in seconds."""
    return now() + ttl_seconds


def is_expired(expiry_timestamp: int) -> bool:
    """Check if timestamp is in the past (expired)."""
    return expiry_timestamp < now()


def metrics_summary(data: Dict[str, Any]) -> str:
    """Format metrics data as human-readable summary."""
    lines = []
    for key, value in data.items():
        if isinstance(value, float) and key.startswith('cost'):
            value = format_cost(value)
        elif isinstance(value, float) and key.endswith('similarity'):
            value = similarity_to_percentage(value)
        lines.append(f"{key}: {value}")
    return "\n".join(lines)
