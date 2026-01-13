"""Custom exceptions for LLMCacheX.

Defines the exception hierarchy for the LLMCacheX caching system.
"""

from typing import Optional


class LLMCacheXError(Exception):
    """Base exception for all LLMCacheX errors."""

    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(message)


class CacheMiss(LLMCacheXError):
    """Raised when a cache key is not found.

    This is expected behavior, not an error in most cases.
    """

    def __init__(self, key: str, message: Optional[str] = None):
        self.key = key
        msg = message or f"Cache miss for key: {key}"
        super().__init__(msg, code="CACHE_MISS")


class CacheHit(Exception):
    """Raised to signal a cache hit (used for control flow)."""

    def __init__(self, value):
        self.value = value
        super().__init__("Cache hit")


class StorageError(LLMCacheXError):
    """Raised when storage backend operations fail."""

    def __init__(self, message: str, backend: Optional[str] = None):
        self.backend = backend
        super().__init__(message, code="STORAGE_ERROR")


class StorageConnectionError(StorageError):
    """Raised when storage connection fails."""

    def __init__(self, backend: str, url: str):
        msg = f"Failed to connect to {backend}: {url}"
        super().__init__(msg, backend)
        self.code = "STORAGE_CONNECTION_ERROR"
        self.url = url


class StorageOperationError(StorageError):
    """Raised when storage operation fails."""

    def __init__(self, operation: str, key: str, message: str):
        msg = f"Storage {operation} failed for key {key}: {message}"
        super().__init__(msg)
        self.code = "STORAGE_OPERATION_ERROR"
        self.operation = operation
        self.key = key


class ProviderError(LLMCacheXError):
    """Raised when provider operations fail."""

    def __init__(self, message: str, provider: Optional[str] = None):
        self.provider = provider
        super().__init__(message, code="PROVIDER_ERROR")


class LLMCallError(ProviderError):
    """Raised when LLM API call fails."""

    def __init__(self, provider: str, model: str, message: str):
        msg = f"LLM call failed ({provider}/{model}): {message}"
        super().__init__(msg, provider)
        self.code = "LLM_CALL_ERROR"
        self.model = model


class EmbeddingGenerationError(ProviderError):
    """Raised when embedding generation fails."""

    def __init__(self, message: str, provider: str = "openai"):
        msg = f"Embedding generation failed: {message}"
        super().__init__(msg, provider)
        self.code = "EMBEDDING_ERROR"


class ConfigurationError(LLMCacheXError):
    """Raised when configuration is invalid."""

    def __init__(self, key: str, message: str):
        msg = f"Configuration error for {key}: {message}"
        super().__init__(msg, code="CONFIG_ERROR")
        self.config_key = key


class ValidationError(LLMCacheXError):
    """Raised when input validation fails."""

    def __init__(self, field: str, message: str):
        msg = f"Validation error for {field}: {message}"
        super().__init__(msg, code="VALIDATION_ERROR")
        self.field = field


class ThresholdError(LLMCacheXError):
    """Raised when similarity threshold is invalid."""

    def __init__(self, threshold: float):
        msg = f"Invalid threshold {threshold}: must be between 0.0 and 1.0"
        super().__init__(msg, code="THRESHOLD_ERROR")
        self.threshold = threshold


class TimeoutError(LLMCacheXError):
    """Raised when operation times out."""

    def __init__(self, operation: str, timeout: float):
        msg = f"Operation '{operation}' timed out after {timeout}s"
        super().__init__(msg, code="TIMEOUT_ERROR")
        self.operation = operation
        self.timeout = timeout
