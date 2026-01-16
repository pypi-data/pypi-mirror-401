"""
Cache module for storing and retrieving command outputs.

The cache is stored in ~/.qlookz/cache/ as individual files,
with filenames derived from hashing the command string.
"""

import hashlib
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class CacheEntry:
    """Represents a cached command output."""
    command: str
    stdout: str
    stderr: str
    exit_code: int
    timestamp: float
    duration: float
    
    @property
    def age_seconds(self) -> float:
        """Return the age of this cache entry in seconds."""
        return time.time() - self.timestamp
    
    @property
    def created_at(self) -> str:
        """Return human-readable creation time."""
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "command": self.command,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "timestamp": self.timestamp,
            "duration": self.duration,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CacheEntry":
        """Create CacheEntry from dictionary."""
        return cls(
            command=data["command"],
            stdout=data["stdout"],
            stderr=data["stderr"],
            exit_code=data["exit_code"],
            timestamp=data["timestamp"],
            duration=data["duration"],
        )


class Cache:
    """
    File-based cache for command outputs.
    
    Each command's output is stored in a separate JSON file,
    named by the SHA-256 hash of the command string.
    """
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize cache with optional custom directory.
        
        Args:
            cache_dir: Custom cache directory. Defaults to ~/.qlookz/cache/
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".qlookz" / "cache"
        self.cache_dir = Path(cache_dir)
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self) -> None:
        """Create cache directory if it doesn't exist."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, command: str) -> str:
        """Generate a cache key (hash) for a command string."""
        return hashlib.sha256(command.encode()).hexdigest()[:16]
    
    def _get_cache_path(self, command: str) -> Path:
        """Get the file path for a command's cache entry."""
        key = self._get_cache_key(command)
        return self.cache_dir / f"{key}.json"
    
    def store(self, entry: CacheEntry) -> Path:
        """
        Store a cache entry.
        
        Args:
            entry: The CacheEntry to store
            
        Returns:
            Path to the cache file
        """
        cache_path = self._get_cache_path(entry.command)
        with open(cache_path, "w") as f:
            json.dump(entry.to_dict(), f, indent=2)
        return cache_path
    
    def lookup(self, command: str) -> Optional[CacheEntry]:
        """
        Look up a cached command output.
        
        Args:
            command: The command string to look up
            
        Returns:
            CacheEntry if found, None otherwise
        """
        cache_path = self._get_cache_path(command)
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path) as f:
                data = json.load(f)
            return CacheEntry.from_dict(data)
        except (json.JSONDecodeError, KeyError, IOError):
            return None
    
    def delete(self, command: str) -> bool:
        """
        Delete a cached command output.
        
        Args:
            command: The command string to delete
            
        Returns:
            True if deleted, False if not found
        """
        cache_path = self._get_cache_path(command)
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False
    
    def clear(self) -> int:
        """
        Clear all cached entries.
        
        Returns:
            Number of entries deleted
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        return count
    
    def list_entries(self) -> list[CacheEntry]:
        """
        List all cached entries.
        
        Returns:
            List of all CacheEntry objects in the cache
        """
        entries = []
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file) as f:
                    data = json.load(f)
                entries.append(CacheEntry.from_dict(data))
            except (json.JSONDecodeError, KeyError, IOError):
                continue
        return sorted(entries, key=lambda e: e.timestamp, reverse=True)
    
    def prune(self, max_age_seconds: float) -> int:
        """
        Remove entries older than max_age_seconds.
        
        Args:
            max_age_seconds: Maximum age in seconds
            
        Returns:
            Number of entries pruned
        """
        count = 0
        cutoff = time.time() - max_age_seconds
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file) as f:
                    data = json.load(f)
                if data.get("timestamp", 0) < cutoff:
                    cache_file.unlink()
                    count += 1
            except (json.JSONDecodeError, KeyError, IOError):
                continue
        return count


# Default cache instance
_default_cache: Optional[Cache] = None


def get_cache() -> Cache:
    """Get the default cache instance."""
    global _default_cache
    if _default_cache is None:
        _default_cache = Cache()
    return _default_cache
