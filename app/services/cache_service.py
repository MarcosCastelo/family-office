"""Cache service for optimizing heavy calculations"""
import time
from typing import Any, Dict, Optional
from functools import wraps
import hashlib
import json

class CacheService:
    """Simple in-memory cache service for asset calculations"""
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self._cache:
            return None
        
        cache_entry = self._cache[key]
        if time.time() > cache_entry['expires_at']:
            del self._cache[key]
            return None
        
        return cache_entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL"""
        ttl = ttl or self.default_ttl
        self._cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl
        }
    
    def delete(self, key: str) -> None:
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache"""
        self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        active_keys = [k for k, v in self._cache.items() if current_time <= v['expires_at']]
        expired_keys = [k for k, v in self._cache.items() if current_time > v['expires_at']]
        
        # Clean expired keys
        for key in expired_keys:
            del self._cache[key]
        
        return {
            'total_keys': len(self._cache),
            'active_keys': len(active_keys),
            'expired_keys': len(expired_keys),
            'memory_usage': len(str(self._cache))
        }

# Global cache instance
asset_cache = CacheService(default_ttl=300)  # 5 minutes for asset calculations

def cached(ttl: Optional[int] = None, key_prefix: str = ""):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create safe cache key from function name and arguments
            # Filter out SQLAlchemy objects and other non-serializable objects
            safe_args = []
            safe_kwargs = {}
            
            for arg in args:
                if hasattr(arg, '__class__') and hasattr(arg.__class__, '__name__'):
                    # For SQLAlchemy objects, use their ID or a safe representation
                    if hasattr(arg, 'id'):
                        safe_args.append(f"{arg.__class__.__name__}:{arg.id}")
                    else:
                        safe_args.append(f"{arg.__class__.__name__}:{str(arg)}")
                else:
                    safe_args.append(str(arg))
            
            for key, value in kwargs.items():
                if hasattr(value, '__class__') and hasattr(value.__class__, '__name__'):
                    # For SQLAlchemy objects, use their ID or a safe representation
                    if hasattr(value, 'id'):
                        safe_kwargs[key] = f"{value.__class__.__name__}:{value.id}"
                    else:
                        safe_kwargs[key] = f"{value.__class__.__name__}:{str(value)}"
                else:
                    safe_kwargs[key] = str(value)
            
            # Create cache key from function name and safe arguments
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(json.dumps((safe_args, safe_kwargs), sort_keys=True).encode()).hexdigest()}"
            
            # Try to get from cache
            cached_result = asset_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            asset_cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

def invalidate_cache_pattern(pattern: str):
    """Invalidate cache keys matching a pattern"""
    keys_to_delete = [k for k in asset_cache._cache.keys() if pattern in k]
    for key in keys_to_delete:
        asset_cache.delete(key)
