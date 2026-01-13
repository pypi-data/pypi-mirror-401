"""Cache eviction and refresh policies."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional
from .utils import now
import heapq


class EvictionPolicy(ABC):
    """Base class for cache eviction policies."""

    @abstractmethod
    def should_evict(self, cache_size: int, max_size: int, entry_count: int) -> bool:
        """Determine if eviction is needed."""
        pass

    @abstractmethod
    def select_victim(self, entries: Dict[str, Any]) -> Optional[str]:
        """Select key to evict."""
        pass


class LRUPolicy(EvictionPolicy):
    """Least Recently Used eviction policy.

    Evicts the entry that hasn't been accessed recently.
    """

    def should_evict(self, cache_size: int, max_size: int, entry_count: int) -> bool:
        return cache_size > max_size

    def select_victim(self, entries: Dict[str, Any]) -> Optional[str]:
        """Find least recently accessed entry."""
        if not entries:
            return None

        # Find entry with oldest last_accessed time
        oldest_key = min(
            entries.keys(),
            key=lambda k: entries[k].get('last_accessed', float('inf'))
        )
        return oldest_key


class LFUPolicy(EvictionPolicy):
    """Least Frequently Used eviction policy.

    Evicts the entry accessed least often.
    """

    def should_evict(self, cache_size: int, max_size: int, entry_count: int) -> bool:
        return cache_size > max_size

    def select_victim(self, entries: Dict[str, Any]) -> Optional[str]:
        """Find least frequently accessed entry."""
        if not entries:
            return None

        # Find entry with lowest access count
        victim_key = min(
            entries.keys(),
            key=lambda k: entries[k].get('access_count', 0)
        )
        return victim_key


class FIFOPolicy(EvictionPolicy):
    """First In First Out eviction policy.

    Evicts the oldest entry (by creation time).
    """

    def should_evict(self, cache_size: int, max_size: int, entry_count: int) -> bool:
        return cache_size > max_size

    def select_victim(self, entries: Dict[str, Any]) -> Optional[str]:
        """Find oldest entry by creation time."""
        if not entries:
            return None

        oldest_key = min(
            entries.keys(),
            key=lambda k: entries[k].get('created_at', float('inf'))
        )
        return oldest_key


class TTLPolicy(EvictionPolicy):
    """Time-To-Live based eviction policy.

    Removes entries that have expired based on TTL.
    """

    def __init__(self, ttl_seconds: int = 86400):
        self.ttl_seconds = ttl_seconds

    def should_evict(self, cache_size: int, max_size: int, entry_count: int) -> bool:
        # TTL eviction is always checked
        return True

    def select_victim(self, entries: Dict[str, Any]) -> Optional[str]:
        """Find expired entries."""
        current_time = now()

        for key, entry in entries.items():
            created_at = entry.get('created_at', 0)
            if current_time - created_at > self.ttl_seconds:
                return key

        return None


class AdaptivePolicy(EvictionPolicy):
    """Adaptive policy that combines multiple strategies.

    Uses a weighted approach:
    - Access frequency: 40%
    - Recency: 40%
    - Cost: 20%
    """

    def should_evict(self, cache_size: int, max_size: int, entry_count: int) -> bool:
        return cache_size > max_size

    def select_victim(self, entries: Dict[str, Any]) -> Optional[str]:
        """Find entry with lowest combined score."""
        if not entries:
            return None

        scores = {}
        current_time = now()

        for key, entry in entries.items():
            # Recency score (newer = higher)
            created_at = entry.get('created_at', 0)
            age = current_time - created_at
            recency = max(0, 1.0 - (age / 86400.0))  # Decay over 1 day

            # Frequency score (higher access = higher)
            frequency = min(1.0, entry.get('access_count', 0) / 100.0)

            # Cost score (higher cost = keep longer)
            cost = min(1.0, entry.get('cost', 0) * 100.0)  # Scale to 0-1

            # Combined score (lower = evict first)
            score = (frequency * 0.4) + (recency * 0.4) + (cost * 0.2)
            scores[key] = score

        # Return key with lowest score
        return min(scores.keys(), key=lambda k: scores[k])


class RefreshPolicy(ABC):
    """Base class for cache refresh policies."""

    @abstractmethod
    def should_refresh(self, entry: Dict[str, Any]) -> bool:
        """Determine if entry should be refreshed."""
        pass


class TimeBasedRefresh(RefreshPolicy):
    """Refresh entries based on age."""

    def __init__(self, max_age_seconds: int = 3600):
        self.max_age = max_age_seconds

    def should_refresh(self, entry: Dict[str, Any]) -> bool:
        created_at = entry.get('created_at', 0)
        age = now() - created_at
        return age > self.max_age


class CostBasedRefresh(RefreshPolicy):
    """Refresh entries based on cost savings.

    Refreshes expensive entries periodically to check for updates.
    """

    def __init__(self, min_cost: float = 0.01, refresh_interval: int = 3600):
        self.min_cost = min_cost
        self.refresh_interval = refresh_interval

    def should_refresh(self, entry: Dict[str, Any]) -> bool:
        cost = entry.get('cost', 0)
        if cost < self.min_cost:
            return False

        created_at = entry.get('created_at', 0)
        age = now() - created_at
        return age > self.refresh_interval


def get_policy(name: str) -> EvictionPolicy:
    """Get eviction policy by name.

    Args:
        name: Policy name (lru, lfu, fifo, ttl, adaptive)

    Returns:
        EvictionPolicy instance
    """
    policies = {
        'lru': LRUPolicy,
        'lfu': LFUPolicy,
        'fifo': FIFOPolicy,
        'ttl': TTLPolicy,
        'adaptive': AdaptivePolicy,
    }

    policy_class = policies.get(name.lower(), LRUPolicy)
    return policy_class()
