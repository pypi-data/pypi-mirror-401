"""Hashing utilities for deterministic cache keys.

Uses SHA256 for consistent, deterministic hashing across requests.
Includes org_id in hash for multi-tenant isolation.
"""

import hashlib
import json
from typing import Union, Dict, Any, Optional
from .exceptions import ValidationError


def hash_request(req) -> str:
    """Generate deterministic SHA256 hash from request.

    Args:
        req: LLMRequest object

    Returns:
        SHA256 hex digest

    The hash includes:
    - org_id (for multi-tenant isolation)
    - provider
    - model
    - prompt (normalized)
    - temperature

    This ensures identical requests from different orgs don't collide.
    """
    try:
        payload = {
            "org_id": req.org_id,
            "provider": req.provider,
            "model": req.model,
            "prompt": req.prompt.strip(),  # Normalize whitespace
            "temperature": req.temperature,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(raw.encode()).hexdigest()
    except (AttributeError, TypeError) as e:
        raise ValidationError("request", f"Invalid request format: {e}")


def hash_prompt(prompt: str, org_id: str = "default") -> str:
    """Generate hash from just prompt text.

    Useful for semantic deduplication where model might differ.
    """
    try:
        payload = {
            "org_id": org_id,
            "prompt": prompt.strip(),
        }
        raw = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(raw.encode()).hexdigest()
    except (AttributeError, TypeError) as e:
        raise ValidationError("prompt", f"Invalid prompt format: {e}")


def hash_dict(data: Dict[str, Any]) -> str:
    """Generate hash from dictionary.

    Args:
        data: Dictionary to hash

    Returns:
        SHA256 hex digest
    """
    try:
        raw = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(raw.encode()).hexdigest()
    except (TypeError, ValueError) as e:
        raise ValidationError("dict", f"Cannot hash dict: {e}")


def hash_string(text: str, algorithm: str = "sha256") -> str:
    """Generate hash from string.

    Args:
        text: Text to hash
        algorithm: Hash algorithm (sha256, md5, sha1)

    Returns:
        Hex digest
    """
    if algorithm not in {"sha256", "md5", "sha1"}:
        raise ValidationError("algorithm", f"Unsupported algorithm: {algorithm}")

    if algorithm == "sha256":
        h = hashlib.sha256()
    elif algorithm == "md5":
        h = hashlib.md5()
    else:  # sha1
        h = hashlib.sha1()

    h.update(text.encode())
    return h.hexdigest()


def verify_hash(data: Union[str, Dict, Any], expected_hash: str, algorithm: str = "sha256") -> bool:
    """Verify data matches expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm to use

    Returns:
        True if hashes match
    """
    if isinstance(data, dict):
        actual_hash = hash_dict(data)
    elif isinstance(data, str):
        actual_hash = hash_string(data, algorithm)
    else:
        actual_hash = hash_string(str(data), algorithm)

    return actual_hash == expected_hash


def hash_embedding(embedding: list) -> str:
    """Generate hash of embedding vector.

    Useful for deduplicating embedding requests.
    """
    try:
        # Round to reduce noise
        rounded = [round(x, 6) for x in embedding]
        raw = json.dumps(rounded, separators=(',', ':'))
        return hashlib.sha256(raw.encode()).hexdigest()
    except (TypeError, ValueError) as e:
        raise ValidationError("embedding", f"Invalid embedding: {e}")
