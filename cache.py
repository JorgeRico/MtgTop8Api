import functools
from cachetools import TTLCache

# Shared cache across all routers: 1000 items, 5-minute TTL
cache = TTLCache(maxsize=1000, ttl=300)


def cached(cache_instance):
    """Async-compatible cache decorator wrapping cachetools TTLCache."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = (func.__module__, func.__name__, args, tuple(sorted(kwargs.items())))
            try:
                if key in cache_instance:
                    return cache_instance[key]
            except TypeError:
                pass
            result = await func(*args, **kwargs)
            try:
                cache_instance[key] = result
            except TypeError:
                pass
            return result
        return wrapper
    return decorator
