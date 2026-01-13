"""Cache interface and orchestration."""

import asyncio
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple
from .hasher import hash_request
from .models import LLMResponse
from .config import mode, semantic_threshold, enable_semantic_cache
from .replay import replay
from .utils import now
from .async_dedupe import InFlightRegistry
from .semantic import find_semantic_match

_inflight = InFlightRegistry()


@dataclass
class CacheResult:
    """Wrapper for cache results with metadata."""

    content: str
    cost: float
    cache_hit: bool
    cache_type: str  # "exact", "semantic", "miss", or "replay"
    similarity: Optional[float] = None
    matched_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "content": self.content,
            "cost": self.cost,
            "cached": self.cache_hit,
            "cache_type": self.cache_type,
            "similarity": self.similarity,
            "matched_key": self.matched_key,
        }


class LLMCache:
    def __init__(self, storage, provider, semantic_enabled: Optional[bool] = None):
        self.storage = storage
        self.provider = provider
        # Allow override, otherwise use config
        self.semantic_enabled = semantic_enabled if semantic_enabled is not None else enable_semantic_cache()

    def run(self, req):
        """Synchronous cache run (legacy, without semantic)."""
        key = hash_request(req)

        if mode() == "replay":
            cached = replay(self.storage, key)
            return cached["content"]

        cached = self.storage.get(key)
        if cached:
            return cached["content"]

        text, cost = self.provider.call(
            req.model, req.prompt, req.temperature
        )

        self.storage.set(key, {
            "content": text,
            "cost": cost,
            "created_at": now(),
            "meta": {
                "cache_type": "exact"
            }
        })

        return text

    async def run_async(
        self,
        req,
        similarity_threshold: Optional[float] = None
    ) -> CacheResult:
        """
        Async cache run with semantic matching support.
        
        Flow:
        1. Check replay mode
        2. Try exact match (O(1), fastest)
        3. Try semantic match if enabled (O(n), fallback)
        4. Call LLM if no match
        5. Store with embedding for future semantic matches
        
        Args:
            req: LLMRequest with prompt, model, etc.
            similarity_threshold: Override default semantic threshold
        
        Returns:
            CacheResult with content and metadata
        """
        key = hash_request(req)
        threshold = similarity_threshold or semantic_threshold()

        # Replay mode
        if mode() == "replay":
            cached = replay(self.storage, key)
            return CacheResult(
                content=cached["content"],
                cost=cached.get("cost", 0.0),
                cache_hit=True,
                cache_type="replay"
            )

        # Step 1: Try exact match (fast path)
        cached = self.storage.get(key)
        if cached:
            return CacheResult(
                content=cached["content"],
                cost=cached.get("cost", 0.0),
                cache_hit=True,
                cache_type="exact",
                matched_key=key
            )

        # Step 2: Try semantic match (if enabled)
        embedding = None
        if self.semantic_enabled:
            # Generate embedding for query
            embedding = await self.provider.generate_embedding(req.prompt)
            
            if embedding:
                match_result = find_semantic_match(
                    self.storage,
                    embedding,
                    threshold,
                    req.org_id
                )
                
                if match_result:
                    matched_key, matched_value, similarity = match_result
                    return CacheResult(
                        content=matched_value["content"],
                        cost=matched_value.get("cost", 0.0),
                        cache_hit=True,
                        cache_type="semantic",
                        similarity=similarity,
                        matched_key=matched_key
                    )

        # Step 3: Cache miss - acquire lock for deduplication
        lock = await _inflight.acquire(key)

        async with lock:
            # Double-check cache (another request may have filled it)
            cached = self.storage.get(key)
            if cached:
                return CacheResult(
                    content=cached["content"],
                    cost=cached.get("cost", 0.0),
                    cache_hit=True,
                    cache_type="exact",
                    matched_key=key
                )

            # Call LLM
            text, cost = await self.provider.call_async(
                req.model, req.prompt, req.temperature
            )

            # Build cache payload
            payload = {
                "content": text,
                "cost": cost,
                "created_at": now(),
                "prompt": req.prompt,  # Store for debugging
                "meta": {
                    "cache_type": "exact",
                    "model": req.model,
                    "org_id": req.org_id
                }
            }

            # Add embedding if semantic is enabled
            if self.semantic_enabled and embedding:
                payload["embedding"] = embedding

            # Store in cache
            self.storage.set(key, payload)
            _inflight.set_result(key, payload)

            return CacheResult(
                content=text,
                cost=cost,
                cache_hit=False,
                cache_type="miss"
            )
