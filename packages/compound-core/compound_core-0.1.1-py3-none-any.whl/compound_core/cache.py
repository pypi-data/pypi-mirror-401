import sqlite3
import json
import hashlib
import time
from pathlib import Path
from functools import wraps
from typing import Any, Optional

# Lazy initialization to avoid import-time side effects in MCP
_CACHE_DB_PATH = None

def _get_cache_db_path():
    global _CACHE_DB_PATH
    if _CACHE_DB_PATH is None:
        from .paths import get_data_path
        _CACHE_DB_PATH = Path(get_data_path("cache/semantic_cache.db"))
    return _CACHE_DB_PATH

def init_cache():
    """Initialize the cache database."""
    cache_path = _get_cache_db_path()
    if not cache_path.parent.exists():
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        
    conn = sqlite3.connect(_get_cache_db_path())
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS function_cache (
            key TEXT PRIMARY KEY,
            value TEXT,
            created_at REAL,
            expires_at REAL
        )
    ''')
    conn.commit()
    conn.close()

def _make_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """Create a stable hash key from function arguments."""
    
    # Pre-process args/kwargs to handle non-serializable objects (like AgentPersona)
    def sanitize(obj):
        if hasattr(obj, "__dict__"):
            return sanitize(obj.__dict__)
        if isinstance(obj, (list, tuple)):
            return [sanitize(i) for i in obj]
        if isinstance(obj, dict):
            return {str(k): sanitize(v) for k, v in obj.items()}
        return obj

    payload = {
        "func": func_name,
        "args": sanitize(args),
        "kwargs": sanitize(kwargs)
    }
    # Sort keys to ensure stability
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def get_cached(key: str) -> Optional[Any]:
    try:
        conn = sqlite3.connect(_get_cache_db_path())
        c = conn.cursor()
        c.execute("SELECT value, expires_at FROM function_cache WHERE key = ?", (key,))
        row = c.fetchone()
        conn.close()
        
        if row:
            value_json, expires_at = row
            if expires_at and time.time() > expires_at:
                return None # Expired
            return json.loads(value_json)
        return None
    except Exception:
        return None # Fail safe

def set_cached(key: str, value: Any, ttl: int = 3600):
    try:
        conn = sqlite3.connect(_get_cache_db_path())
        c = conn.cursor()
        expires_at = time.time() + ttl
        value_json = json.dumps(value)
        c.execute(
            "INSERT OR REPLACE INTO function_cache (key, value, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (key, value_json, time.time(), expires_at)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass # Fail safe

def unified_cache(ttl_seconds: int = 3600):
    """
    Decorator to cache function results in SQLite.
    Usage:
        @unified_cache(ttl_seconds=300)
        def expensive_op(x): ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Init DB lazily
            init_cache()
            
            key = _make_key(func.__name__, args, kwargs)
            cached = get_cached(key)
            if cached is not None:
                return cached
            
            result = func(*args, **kwargs)
            set_cached(key, result, ttl=ttl_seconds)
            return result
        return wrapper
    return decorator

def unified_cache_async(ttl_seconds: int = 86400):
    """
    Decorator to cache async function results in SQLite.
    Usage:
        @unified_cache_async(ttl_seconds=300)
        async def expensive_op(x): ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Init DB lazily
            init_cache()
            
            key = _make_key(func.__name__, args, kwargs)
            cached = get_cached(key)
            if cached is not None:
                # To distinguish from real execution results in AgentResult
                if isinstance(cached, dict) and "agent_name" in cached:
                    from .types import AgentResult
                    cached_res = AgentResult(**cached)
                    cached_res.cached = True
                    return cached_res
                return cached
            
            result = await func(*args, **kwargs)
            
            # If it's an AgentResult, convert to dict for storage
            storage_val = result
            if hasattr(result, "__dict__"):
                storage_val = result.__dict__
                
            set_cached(key, storage_val, ttl=ttl_seconds)
            return result
        return wrapper
    return decorator
