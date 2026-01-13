"""Configuration helpers for LLMCacheX."""

import os


def mode():
    """Get cache mode: live or replay."""
    return os.getenv("LLMCACHEX_MODE", "live")  # live | replay


def storage_backend():
    """Get storage backend type."""
    return os.getenv("LLMCACHEX_STORAGE", "memory")


def org_id():
    """Get default organization ID."""
    return os.getenv("LLMCACHEX_ORG", "default")


def enable_semantic_cache() -> bool:
    """Check if semantic caching is enabled."""
    return os.getenv("LLMCACHEX_SEMANTIC", "true").lower() in ("true", "1", "yes")


def semantic_threshold() -> float:
    """Get semantic similarity threshold (0.0-1.0).
    
    Default: 0.92
    - 0.90-0.93: Good balance (recommended)
    - 0.94-0.97: More conservative
    - 0.85-0.89: More aggressive (higher hit rate, more false positives)
    """
    try:
        threshold = float(os.getenv("LLMCACHEX_SEMANTIC_THRESHOLD", "0.92"))
        # Clamp to valid range
        return max(0.0, min(1.0, threshold))
    except ValueError:
        return 0.92


def embedding_model() -> str:
    """Get embedding model to use.
    
    Options:
    - text-embedding-3-small (default, cost-efficient)
    - text-embedding-3-large (higher quality, more expensive)
    """
    return os.getenv("LLMCACHEX_EMBEDDING_MODEL", "text-embedding-3-small")
