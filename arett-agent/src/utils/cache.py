from functools import lru_cache


@lru_cache(maxsize=256)
def ttl_cache_key(key: str) -> str:
    """Placeholder cache helper for deterministic cache keys."""
    return key
