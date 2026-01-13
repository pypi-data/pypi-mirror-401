from .client import Limesrail

__all__ = ["Limesrail"]

# Optional: Helper for singleton usage if you support `limesrail.init()`
_global_client = None

def init(api_key: str, **kwargs):
    global _global_client
    _global_client = Limesrail(api_key=api_key, **kwargs)
    return _global_client

def trace(*args, **kwargs):
    if not _global_client:
        raise RuntimeError("Limesrail not initialized. Call limesrail.init() first.")
    return _global_client.trace(*args, **kwargs)

__all__ = ["Limesrail", "init", "trace"]