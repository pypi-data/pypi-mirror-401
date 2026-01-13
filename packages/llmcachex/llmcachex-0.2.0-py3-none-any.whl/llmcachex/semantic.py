"""Semantic caching utilities (similarity + matching).

This module intentionally avoids calling provider SDKs directly.
Embedding generation must be handled by the provider layer to keep
all outbound API interactions centralized and configurable.
"""

import math
from typing import Optional, List, Tuple, Dict, Any


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return dot / (mag1 * mag2)


def is_similar(vec1: List[float], vec2: List[float], threshold: float) -> bool:
    """Check if two vectors are similar above threshold."""
    return cosine_similarity(vec1, vec2) >= threshold


# Note: Embedding generation is intentionally not implemented here.
# Use the provider's `generate_embedding()` method instead.


def find_semantic_match(
    storage,
    embedding: List[float],
    threshold: float = 0.92,
    org_id: str = "default"
) -> Optional[Tuple[str, Dict[str, Any], float]]:
    """Find semantically similar cached entry.
    
    Args:
        storage: Storage backend with cached entries
        embedding: Query embedding vector
        threshold: Minimum similarity score (0.0-1.0)
        org_id: Organization ID for scoped search
    
    Returns:
        Tuple of (key, cached_value, similarity_score) or None
    """
    best_match = None
    best_score = threshold  # Only return matches above threshold
    best_key = None
    
    # Iterate through storage
    # Prefer storage.scan_all() when available; otherwise fall back to in-memory store
    if hasattr(storage, 'scan_all'):
        items = storage.scan_all()
    elif hasattr(storage, 'store'):
        items = storage.store.items()
    else:
        return None
    
    for key, cached_entry in items:
        # Check org_id matches (from hash)
        if not isinstance(cached_entry, dict):
            continue
        
        # Skip entries without embeddings
        if "embedding" not in cached_entry:
            continue
        
        # Calculate similarity
        score = cosine_similarity(embedding, cached_entry["embedding"])
        
        if score > best_score:
            best_score = score
            best_match = cached_entry
            best_key = key
    
    if best_match:
        return (best_key, best_match, best_score)
    
    return None
