import os
import json
import hashlib
from typing import Dict

CACHE_FILENAME = ".assumeless_cache"

class FileHashCache:
    """
    Manages file hash caching to skip unchanged files during scan.
    Stores absolute path -> md5 hash.
    """
    def __init__(self, root_path: str = "."):
        self.root_path = os.path.abspath(root_path)
        self.cache_path = os.path.join(self.root_path, CACHE_FILENAME)
        self.cache: Dict[str, str] = {}
        self.dirty = False

    def load(self) -> None:
        """Load cache from disk."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r") as f:
                    self.cache = json.load(f)
            except Exception:
                self.cache = {}
        else:
            self.cache = {}

    def save(self) -> None:
        """Save cache to disk if modified."""
        if self.dirty:
            try:
                with open(self.cache_path, "w") as f:
                    json.dump(self.cache, f, indent=2)
            except Exception:
                pass # Fail silently for cache write errors usually

    def check_changed(self, file_path: str, content: str) -> bool:
        """
        Returns True if file has changed since last scan (or is new).
        Returns False if file is unchanged.
        """
        abs_path = os.path.abspath(file_path)
        current_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        
        stored_hash = self.cache.get(abs_path)
        
        if stored_hash == current_hash:
            return False
            
        return True

    def update(self, file_path: str, content: str) -> None:
        """Updates the cache with the new hash for the file."""
        abs_path = os.path.abspath(file_path)
        current_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        self.cache[abs_path] = current_hash
        self.dirty = True
