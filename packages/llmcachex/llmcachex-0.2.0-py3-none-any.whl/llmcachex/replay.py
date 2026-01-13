"""Request/response replay helpers for time-travel debugging.

Replay mode allows you to:
- Record LLM responses in production
- Replay them locally with zero API usage
- Debug issues without paying for LLM calls
"""

from typing import Optional, Dict, Any
from .exceptions import CacheMiss
from .utils import now, now_iso, is_expired


class ReplayRecord:
    """A recorded request/response for replay."""

    def __init__(
        self,
        key: str,
        content: str,
        cost: float,
        model: str,
        provider: str,
        prompt: str,
        temperature: float,
        org_id: str = "default",
    ):
        self.key = key
        self.content = content
        self.cost = cost
        self.model = model
        self.provider = provider
        self.prompt = prompt
        self.temperature = temperature
        self.org_id = org_id
        self.recorded_at = now()
        self.recorded_at_iso = now_iso()
        self.replay_count = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "key": self.key,
            "content": self.content,
            "cost": self.cost,
            "model": self.model,
            "provider": self.provider,
            "prompt": self.prompt,
            "temperature": self.temperature,
            "org_id": self.org_id,
            "recorded_at": self.recorded_at,
            "recorded_at_iso": self.recorded_at_iso,
            "replay_count": self.replay_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReplayRecord":
        """Create from dictionary."""
        record = cls(
            key=data["key"],
            content=data["content"],
            cost=data["cost"],
            model=data["model"],
            provider=data["provider"],
            prompt=data["prompt"],
            temperature=data["temperature"],
            org_id=data.get("org_id", "default"),
        )
        record.recorded_at = data.get("recorded_at", now())
        record.recorded_at_iso = data.get("recorded_at_iso", now_iso())
        record.replay_count = data.get("replay_count", 0)
        return record


def replay(storage, key: str, strict: bool = True) -> Dict[str, Any]:
    """Retrieve cached value for replay.

    Args:
        storage: Storage backend
        key: Cache key
        strict: If True, raise error on miss; if False, return None

    Returns:
        Cached entry dict

    Raises:
        CacheMiss: If key not found and strict=True
    """
    value = storage.get(key)

    if value is None:
        if strict:
            raise CacheMiss(key, "Replay failed: cache miss")
        return None

    # Check if entry is expired
    if "expiry" in value:
        if is_expired(value["expiry"]):
            if strict:
                raise CacheMiss(key, "Replay failed: entry expired")
            return None

    return value


def replay_batch(
    storage,
    keys: list,
    allow_misses: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Replay multiple cached entries.

    Args:
        storage: Storage backend
        keys: List of cache keys
        allow_misses: If True, skip missing entries; if False, raise on first miss

    Returns:
        Dict mapping keys to cached values

    Raises:
        CacheMiss: If key not found and allow_misses=False
    """
    results = {}

    for key in keys:
        try:
            value = replay(storage, key, strict=True)
            if value:
                results[key] = value
        except CacheMiss:
            if not allow_misses:
                raise
            # Skip this key
            continue

    return results


def get_replay_stats(storage) -> Dict[str, Any]:
    """Get replay statistics from storage.

    Args:
        storage: Storage backend

    Returns:
        Statistics dict
    """
    stats = {
        "total_entries": 0,
        "expired_entries": 0,
        "valid_entries": 0,
        "total_cost_saved": 0.0,
        "oldest_entry": None,
        "newest_entry": None,
    }

    if not hasattr(storage, 'scan_all'):
        return stats

    entries = storage.scan_all()
    current_time = now()

    for key, entry in entries:
        stats["total_entries"] += 1
        cost = entry.get("cost", 0)
        stats["total_cost_saved"] += cost

        # Check expiry
        if "expiry" in entry and entry["expiry"] < current_time:
            stats["expired_entries"] += 1
        else:
            stats["valid_entries"] += 1

        # Track oldest/newest
        created_at = entry.get("created_at", current_time)
        if stats["oldest_entry"] is None or created_at < stats["oldest_entry"]:
            stats["oldest_entry"] = created_at
        if stats["newest_entry"] is None or created_at > stats["newest_entry"]:
            stats["newest_entry"] = created_at

    return stats
