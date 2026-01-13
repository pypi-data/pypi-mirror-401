"""
Centralized Limits Loader

Provides a single interface to access all system limits from config/limits/*.yaml.
Caches loaded config for performance.
"""
import yaml
from pathlib import Path
from functools import lru_cache
from typing import Any, Optional
import os

# Allow override via environment variable for testing
_CONFIG_DIR_OVERRIDE: Optional[str] = None


def set_config_dir(path: str) -> None:
    """Override config directory (for testing)."""
    global _CONFIG_DIR_OVERRIDE
    _CONFIG_DIR_OVERRIDE = path
    _load_all_limits.cache_clear()


def _get_config_dir() -> Path:
    """Get the config directory path."""
    if _CONFIG_DIR_OVERRIDE:
        return Path(_CONFIG_DIR_OVERRIDE)
        
    try:
        from .paths import get_repo_root
        return get_repo_root() / "config" / "limits"
    except ImportError:
        # Fallback if in a weird state
        return Path(__file__).parent.parent.parent / "config" / "limits"


@lru_cache(maxsize=1)
def _load_all_limits() -> dict:
    """Load and cache all limit files."""
    config_dir = _get_config_dir()
    limits = {}
    
    if not config_dir.exists():
        return limits
        
    for file in config_dir.glob("*.yaml"):
        try:
            with open(file) as f:
                data = yaml.safe_load(f)
                if data:
                    limits[file.stem] = data
        except Exception as e:
            print(f"Warning: Failed to load {file}: {e}")
    
    return limits


def get_limit(path: str, default: Any = None) -> Any:
    """
    Get a limit value by dotted path.
    
    Args:
        path: Dotted path like 'swarm.agents.max_agents' or 'safety.rate_limits.cognitive_per_hour'
        default: Value to return if path not found
        
    Returns:
        The limit value or default
        
    Examples:
        >>> get_limit('swarm.agents.max_agents', 50)
        50
        >>> get_limit('performance.timeouts.debate_initial', 60)
        60
    """
    parts = path.split('.')
    data = _load_all_limits()
    
    for p in parts:
        if isinstance(data, dict):
            data = data.get(p)
            if data is None:
                return default
        else:
            return default
    
    return data if data is not None else default


def get_all_limits() -> dict:
    """Get all loaded limits (for debugging/inspection)."""
    return _load_all_limits()


def reload_limits() -> None:
    """Force reload of all limit files (useful after config changes)."""
    _load_all_limits.cache_clear()


# Convenience accessors for common limits
def get_swarm_limit(key: str, default: Any = None) -> Any:
    """Shortcut for swarm limits."""
    return get_limit(f"swarm.{key}", default)


def get_timeout(key: str, default: int = 60) -> int:
    """Shortcut for performance timeouts."""
    return get_limit(f"performance.timeouts.{key}", default)


def get_rate_limit(key: str, default: int = 10) -> int:
    """Shortcut for safety rate limits."""
    return get_limit(f"safety.rate_limits.{key}", default)
