"""Data models for LLM requests, responses, and cache metadata."""

from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class LLMRequest:
    """Request to be cached/processed.

    Attributes:
        provider: LLM provider (openai, anthropic, cohere)
        model: Model name (gpt-4, gpt-3.5-turbo)
        prompt: Input prompt text
        temperature: Sampling temperature (0.0-2.0)
        org_id: Organization ID for multi-tenancy
        metadata: Additional metadata for tracking
    """

    provider: str
    model: str
    prompt: str
    temperature: float
    org_id: str = "default"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate request."""
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError(f"Temperature must be 0-2.0, got {self.temperature}")
        if not self.prompt or not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
        if not self.model:
            raise ValueError("Model must be specified")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMRequest":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class LLMResponse:
    """LLM response with metadata.

    Attributes:
        content: Response text
        cost: Cost in dollars
        created_at: Unix timestamp
        model: Model used
        provider: Provider used
        usage: Token usage info
    """

    content: str
    cost: float
    created_at: int
    model: str = "unknown"
    provider: str = "unknown"
    usage: Optional[Dict[str, int]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMResponse":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class CacheMeta:
    """Cache metadata.

    Attributes:
        cache_type: Type of cache hit (exact, semantic, miss)
        similarity: Similarity score for semantic matches (0-1)
        matched_key: Key of matched entry
        created_at: When entry was cached
        accessed_at: When entry was last accessed
        access_count: Number of times accessed
    """

    cache_type: str
    similarity: Optional[float] = None
    matched_key: Optional[str] = None
    created_at: Optional[int] = None
    accessed_at: Optional[int] = None
    access_count: int = 0

    def __post_init__(self):
        """Validate metadata."""
        valid_types = {"exact", "semantic", "miss", "replay"}
        if self.cache_type not in valid_types:
            raise ValueError(f"Invalid cache_type: {self.cache_type}")

        if self.similarity is not None:
            if not 0.0 <= self.similarity <= 1.0:
                raise ValueError(f"Similarity must be 0-1, got {self.similarity}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CacheMeta":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class CacheEntry:
    """Complete cache entry with content and metadata.

    Attributes:
        key: Cache key (SHA256 hash)
        content: Response content
        cost: Cost in dollars
        metadata: Cache metadata
        embedding: Embedding vector for semantic search
        created_at: Creation timestamp
        ttl: Time-to-live in seconds (0 = infinite)
    """

    key: str
    content: str
    cost: float
    metadata: CacheMeta
    embedding: Optional[List[float]] = None
    created_at: int = field(default_factory=lambda: __import__('time').time())
    ttl: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "key": self.key,
            "content": self.content,
            "cost": self.cost,
            "metadata": self.metadata.to_dict(),
            "embedding": self.embedding,
            "created_at": self.created_at,
            "ttl": self.ttl,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CacheEntry":
        """Create from dictionary."""
        return cls(
            key=data["key"],
            content=data["content"],
            cost=data["cost"],
            metadata=CacheMeta.from_dict(data["metadata"]),
            embedding=data.get("embedding"),
            created_at=data.get("created_at", int(__import__('time').time())),
            ttl=data.get("ttl", 0),
        )