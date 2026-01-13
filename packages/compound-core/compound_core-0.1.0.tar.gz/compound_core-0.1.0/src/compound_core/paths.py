#!/usr/bin/env python3
"""
Shared Path Resolver for Compound System Scripts.

Provides consistent absolute paths regardless of the current working directory.
All paths are resolved relative to the repository root (3 levels up from this file).

Usage:
    from scripts.lib.path_resolver import get_repo_root, get_data_path, get_analysis_path
    
    data_file = get_data_path("memory.db")  # -> {repo_root}/.agent/data/memory.db
    analysis_file = get_analysis_path("ab-tests/results.db")  # -> {repo_root}/analysis/ab-tests/results.db
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

def resolve_safe_path(base_dir: Path, subpath: str) -> Path:
    """
    Safely resolves a subpath relative to a base directory.
    Enforces security by:
    1. Rejecting absolute paths.
    2. Canonicalizing paths to resolve symlinks (os.path.realpath).
    3. Rejecting ".." patterns and null bytes.
    4. Verifying the result is still contained within the base directory.
    
    Args:
        base_dir: The directory that must contain the result.
        subpath: The relative path to resolve.
        
    Returns:
        The absolute resolved Path (canonicalized).
        
    Raises:
        ValueError: If a security violation or resolution error occurs.
    """
    if not subpath:
        return base_dir.resolve()

    # 1. Reject absolute paths immediately
    if Path(subpath).is_absolute() or subpath.startswith("/"):
        logger.error(f"Security Violation: Absolute path not allowed: {subpath}")
        raise ValueError(f"Security Violation: Absolute path not allowed: {subpath}")
    
    # 2. Reject '..' patterns and null bytes
    if ".." in subpath or "\0" in subpath:
        logger.error(f"Security Violation: Invalid characters or traversal pattern in path: {subpath}")
        raise ValueError(f"Security Violation: Invalid characters or traversal pattern in path: {subpath}")

    # 3. Join and canonicalize
    base_canonical = base_dir.resolve()
    target = (base_canonical / subpath).resolve()
    
    # Use realpath to catch symlink escapes
    target_real = Path(os.path.realpath(target))
    base_real = Path(os.path.realpath(base_canonical))

    # 4. Verify containment
    if not target_real.is_relative_to(base_real):
        logger.error(f"Security Violation: Path traversal detected! {subpath} resolved to {target_real} which is outside {base_real}")
        raise ValueError(f"Security Violation: Path traversal detected! {subpath} is outside {base_real}")
    
    return target_real


def get_repo_root() -> Path:
    """
    Get absolute path to repository root.
    Prioritizes COMPOUND_ROOT env var, then searches for .git/GEMINI.md, then falls back to CWD.
    """
    if "COMPOUND_ROOT" in os.environ:
        path = Path(os.environ["COMPOUND_ROOT"]).resolve()
        if not path.is_dir():
             logger.warning(f"COMPOUND_ROOT is set to {path} but it is not a directory. Ignoring.")
        else:
             return path
        
    # Search upwards for marker
    try:
        current = Path.cwd().resolve()
        for _ in range(10): # Max depth
            if (current / ".git").exists() or (current / "GEMINI.md").exists():
                return current
            if current.parent == current: # Reached root
                break
            current = current.parent
    except Exception as e:
        logger.error(f"Error resolving repo root from CWD: {e}")

    # Fallback: Check relative to this file
    try:
        current = Path(__file__).resolve()
        for _ in range(10):
            if (current / ".git").exists() or (current / "GEMINI.md").exists():
                return current
            if current.parent == current:
                break
            current = current.parent
    except Exception as e:
        logger.error(f"Error resolving repo root from __file__: {e}")
        
    # Final safety guard
    result = Path.cwd().resolve()
    if result == Path("/") or str(result) == "/":
        raise RuntimeError(
            "CRITICAL: get_repo_root() resolved to system root '/'. "
            "Set COMPOUND_ROOT environment variable or ensure .git/GEMINI.md exists in your project."
        )
        
    # Fallback
    logger.debug("Could not find repo root marker (.git or GEMINI.md). defaulting to CWD.")
    return Path.cwd().resolve()


def get_data_path(filename: str) -> str:
    """
    Get absolute path to a file in .agent/data/.
    Creates directory if it doesn't exist.
    """
    data_dir = get_repo_root() / ".agent" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(resolve_safe_path(data_dir, filename))


def get_analysis_path(subpath: str) -> str:
    """
    Get absolute path to a file in analysis/.
    Creates parent directories if they don't exist.
    """
    analysis_dir = get_repo_root() / "analysis"
    return str(resolve_safe_path(analysis_dir, subpath))


def get_skills_path(subpath: str) -> str:
    """Get absolute path to a file in skills/."""
    skills_dir = get_repo_root() / "skills"
    return str(resolve_safe_path(skills_dir, subpath))


def get_config_path(filename: str) -> str:
    """
    Get absolute path to a config file in .agent/.
    Creates directory if it doesn't exist.
    """
    config_dir = get_repo_root() / ".agent"
    config_dir.mkdir(parents=True, exist_ok=True)
    return str(resolve_safe_path(config_dir, filename))
