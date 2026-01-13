"""LLMCacheX - Intelligent caching layer for LLM calls.

Features:
- Exact match caching with deterministic hashing
- Semantic caching with embeddings
- Async deduplication for concurrent requests
- Org-scoped multi-tenancy
- Replay/time-travel debugging
- Cost tracking and control
"""

__version__ = "0.2.0"
__author__ = "prabhnoor12"
__license__ = "MIT"

from .cache import LLMCache, CacheResult
from .models import LLMRequest, LLMResponse, CacheMeta
from .exceptions import (
    LLMCacheXError,
    CacheMiss,
    CacheHit,
    EmbeddingGenerationError,
    StorageError,
    ProviderError,
)
from .storage.base import BaseStorage
from .storage.memory import MemoryStorage
from .storage.redis import RedisStorage

__all__ = [
    # Version
    "__version__",
    # Core
    "LLMCache",
    "CacheResult",
    # Models
    "LLMRequest",
    "LLMResponse",
    "CacheMeta",
    # Exceptions
    "LLMCacheXError",
    "CacheMiss",
    "CacheHit",
    "EmbeddingGenerationError",
    "StorageError",
    "ProviderError",
    # Storage
    "BaseStorage",
    "MemoryStorage",
    "RedisStorage",
]
