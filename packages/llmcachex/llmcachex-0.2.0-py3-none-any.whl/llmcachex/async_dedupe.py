"""Async in-flight request deduplication.

This module provides efficient deduplication of concurrent requests to prevent
duplicate API calls and resource waste. When multiple concurrent requests with
the same parameters arrive, they are deduplicated to use a single underlying
request with results shared across all callers.

Key Features:
- Thread-safe and async-safe concurrent request handling
- Automatic cleanup of completed requests
- Result sharing across duplicate requests
- Exception propagation to all waiting callers
- Memory-efficient with bounded cache
- Metrics and monitoring support
- Configurable expiry and cleanup strategies
"""

import asyncio
import logging
import time
from typing import Any, Dict, Optional, Callable, Coroutine, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
import weakref

logger = logging.getLogger(__name__)

T = TypeVar('T')


class RequestStatus(Enum):
    """Status of an in-flight request."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class RequestMetadata:
    """Metadata for tracking in-flight requests.
    
    Attributes:
        key: Unique request identifier.
        status: Current request status.
        created_at: Timestamp when request was created.
        completed_at: Timestamp when request completed.
        result: Cached result value.
        exception: Exception raised during execution.
        waiters: Count of tasks waiting for this request.
        caller_count: Total number of callers deduplicated.
    """
    key: str
    status: RequestStatus = RequestStatus.PENDING
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    result: Any = None
    exception: Optional[Exception] = None
    waiters: int = 0
    caller_count: int = 1
    
    @property
    def duration(self) -> Optional[float]:
        """Get request duration in seconds."""
        if self.completed_at:
            return self.completed_at - self.created_at
        return None
    
    @property
    def is_complete(self) -> bool:
        """Check if request has completed."""
        return self.status in (RequestStatus.COMPLETED, RequestStatus.FAILED, RequestStatus.CANCELLED)


class InFlightRegistry(Generic[T]):
    """Thread-safe async request deduplication registry.
    
    Deduplicates concurrent requests with identical keys by routing them through
    a single underlying request execution. Results and exceptions are shared
    across all waiting callers.
    
    Example:
        registry = InFlightRegistry(max_entries=10000)
        
        # Multiple concurrent requests with same key use one API call
        result = await registry.execute_once("user-123", fetch_user_data)
        
    Attributes:
        _locks: Mapping of request keys to asyncio locks.
        _results: Mapping of request keys to metadata.
        _max_entries: Maximum number of cached results before cleanup.
        _expiry_seconds: Time to keep completed results (None = infinite).
    """
    
    def __init__(
        self,
        max_entries: int = 10000,
        expiry_seconds: Optional[float] = None
    ) -> None:
        """Initialize the in-flight request registry.
        
        Args:
            max_entries: Maximum number of stored results before cleanup (default: 10000).
            expiry_seconds: Auto-expiry time for completed results in seconds.
                           None = results persist until manually cleared.
        \n        Raises:
            ValueError: If max_entries < 1.
        """
        if max_entries < 1:
            raise ValueError("max_entries must be at least 1")
        
        self._locks: Dict[str, asyncio.Lock] = {}
        self._results: Dict[str, RequestMetadata] = {}
        self._max_entries = max_entries
        self._expiry_seconds = expiry_seconds
        self._lock = asyncio.Lock()  # Protects dict modifications
        self._stats = {
            "total_requests": 0,
            "deduplicated": 0,
            "completed": 0,
            "failed": 0,
            "cache_hits": 0
        }
        
        logger.info(
            f"InFlightRegistry initialized: max_entries={max_entries}, "
            f"expiry_seconds={expiry_seconds}"
        )

    async def acquire(self, key: str) -> asyncio.Lock:
        """Acquire or create a lock for the given key.
        
        Creates a new lock if one doesn't exist. Thread-safe for concurrent access.
        
        Args:
            key: Unique identifier for the request.
            
        Returns:
            asyncio.Lock: Lock associated with this key.
        """
        async with self._lock:
            if key not in self._locks:
                self._locks[key] = asyncio.Lock()
                logger.debug(f"Created new lock for key: {key}")
            return self._locks[key]

    def set_result(self, key: str, value: Any, status: RequestStatus = RequestStatus.COMPLETED) -> None:
        """Store result for a completed request.
        
        Args:
            key: Request identifier.
            value: Result value or exception object.
            status: Request status (COMPLETED or FAILED).
            
        Raises:
            ValueError: If status is not terminal.
        """
        if status not in (RequestStatus.COMPLETED, RequestStatus.FAILED):
            raise ValueError(f"Cannot set result for non-terminal status: {status}")
        
        if key in self._results:
            metadata = self._results[key]
            if isinstance(value, Exception):
                metadata.exception = value
                metadata.status = RequestStatus.FAILED
            else:
                metadata.result = value
                metadata.status = RequestStatus.COMPLETED
            
            metadata.completed_at = time.time()
            logger.debug(
                f"Result set for key {key}: status={status}, "
                f"duration={metadata.duration:.3f}s, waiters={metadata.waiters}"
            )
            
            self._stats["completed" if status == RequestStatus.COMPLETED else "failed"] += 1

    def get_result(self, key: str) -> Optional[Any]:
        """Retrieve result for a completed request.
        
        Returns None if result doesn't exist or request still pending.
        
        Args:
            key: Request identifier.
            
        Returns:
            Cached result value, or None if not found/pending.
        """
        metadata = self._results.get(key)
        if metadata:
            self._stats["cache_hits"] += 1
            return metadata.result
        return None

    def get_exception(self, key: str) -> Optional[Exception]:
        """Retrieve exception from a failed request.
        
        Args:
            key: Request identifier.
            
        Returns:
            Exception object, or None if request succeeded/doesn't exist.
        """
        metadata = self._results.get(key)
        if metadata and metadata.status == RequestStatus.FAILED:
            return metadata.exception
        return None

    def get_metadata(self, key: str) -> Optional[RequestMetadata]:
        """Get complete metadata for a request.
        
        Args:
            key: Request identifier.
            
        Returns:
            RequestMetadata object, or None if not found.
        """
        return self._results.get(key)

    async def clear(self, key: str) -> None:
        """Clear lock and result for a request.
        
        Safe to call even if key doesn't exist (idempotent).
        
        Args:
            key: Request identifier to clear.
        """
        async with self._lock:
            self._locks.pop(key, None)
            self._results.pop(key, None)
            logger.debug(f"Cleared lock and result for key: {key}")

    async def execute_once(
        self,
        key: str,
        coroutine_fn: Callable[[], Coroutine[Any, Any, T]]
    ) -> T:
        """Execute coroutine once, deduplicate concurrent requests.
        
        If another request with the same key is in-flight, waits for that result
        instead of executing the coroutine again. Exceptions are propagated.
        
        Example:
            async def fetch_user():
                return await api.get_user(user_id)
            
            # Multiple concurrent calls with same key use one fetch
            user = await registry.execute_once("user-123", fetch_user)
            
        Args:
            key: Unique identifier for this request.
            coroutine_fn: Callable that returns a coroutine to execute.
            
        Returns:
            Result from the coroutine execution.
            
        Raises:
            Exception: Any exception raised by the coroutine.
        """
        lock = await self.acquire(key)
        
        async with lock:
            # Check if result already exists (from previous execution)
            if key in self._results:
                metadata = self._results[key]
                
                if metadata.is_complete:
                    logger.debug(
                        f"Returning cached result for key {key}: "
                        f"status={metadata.status}"
                    )
                    
                    if metadata.exception:
                        raise metadata.exception
                    
                    return metadata.result
            
            # Initialize metadata for this execution
            if key not in self._results:
                self._results[key] = RequestMetadata(key=key, caller_count=1)
                self._stats["total_requests"] += 1
            else:
                self._results[key].caller_count += 1
                self._stats["deduplicated"] += 1
            
            metadata = self._results[key]
            
            logger.debug(
                f"Executing request for key {key} "
                f"(dedup count: {metadata.caller_count})"
            )
            
            # Execute the coroutine
            try:
                result = await coroutine_fn()
                self.set_result(key, result, RequestStatus.COMPLETED)
                return result
            except Exception as e:
                logger.error(f"Request failed for key {key}: {e}")
                self.set_result(key, e, RequestStatus.FAILED)
                raise

    async def cleanup_expired(self) -> int:
        """Remove expired completed results to free memory.
        
        Only removes results older than expiry_seconds. Results without expiry
        are not removed. Should be called periodically.
        
        Returns:
            Number of entries cleaned up.
        """
        if self._expiry_seconds is None:
            return 0
        
        current_time = time.time()
        expired_keys = []
        
        async with self._lock:
            for key, metadata in list(self._results.items()):
                if (
                    metadata.is_complete and
                    metadata.completed_at and
                    (current_time - metadata.completed_at) > self._expiry_seconds
                ):
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._locks.pop(key, None)
                self._results.pop(key, None)
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired entries")
        
        return len(expired_keys)

    async def cleanup_lru(self) -> int:
        """Clean up oldest completed results if cache exceeds max_entries.
        
        Removes completed results in LRU (least recently completed) order.
        In-flight and recent results are preserved.
        
        Returns:
            Number of entries cleaned up.
        """
        async with self._lock:
            if len(self._results) <= self._max_entries:
                return 0
            
            # Find completed results sorted by completion time
            completed = [
                (key, metadata) for key, metadata in self._results.items()
                if metadata.is_complete
            ]
            
            if not completed:
                logger.warning("Cache full but no completed results to clean")
                return 0
            
            # Sort by completion time, oldest first
            completed.sort(key=lambda x: x[1].completed_at or 0)
            
            # Remove oldest until below threshold
            to_remove = len(self._results) - self._max_entries + 100
            removed_keys = [key for key, _ in completed[:to_remove]]
            
            for key in removed_keys:
                self._locks.pop(key, None)
                self._results.pop(key, None)
        
        logger.info(f"LRU cleanup: removed {len(removed_keys)} entries")
        return len(removed_keys)

    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics.
        
        Returns:
            dict: Statistics including request counts and deduplication metrics.
        """
        return {
            **self._stats,
            "active_entries": len(self._results),
            "active_locks": len(self._locks),
            "total_waiters": sum(
                m.waiters for m in self._results.values()
            )
        }

    async def health_check(self) -> bool:
        """Check registry health.
        
        Verifies that locks are properly managed and no deadlocks.
        
        Returns:
            bool: True if healthy, False otherwise.
        """
        try:
            test_key = "__health_check__"
            await self.execute_once(test_key, lambda: asyncio.sleep(0))
            await self.clear(test_key)
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
