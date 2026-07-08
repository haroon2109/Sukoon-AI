import os
import json
import logging
import hashlib
from typing import Optional, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class CacheProvider(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass
        
    @abstractmethod
    def set(self, key: str, value: str, ttl: int = 3600):
        pass

class InMemoryCache(CacheProvider):
    def __init__(self):
        try:
            from cachetools import TTLCache
            self.cache = TTLCache(maxsize=1000, ttl=3600)
        except ImportError:
            self.cache = {}
            logger.warning("cachetools not installed. Falling back to unbounded dict cache without TTL.")

    def get(self, key: str) -> Optional[str]:
        return self.cache.get(key)
        
    def set(self, key: str, value: str, ttl: int = 3600):
        # TTLCache ignores per-key TTL; just stores it
        self.cache[key] = value

class RedisCache(CacheProvider):
    def __init__(self, redis_url: str):
        try:
            import redis
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
        except ImportError:
            logger.error("redis-py not installed but REDIS_URL is provided.")
            self.client = None

    def get(self, key: str) -> Optional[str]:
        if self.client:
            try:
                return self.client.get(key)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        return None
        
    def set(self, key: str, value: str, ttl: int = 3600):
        if self.client:
            try:
                self.client.setex(key, ttl, value)
            except Exception as e:
                logger.error(f"Redis set error: {e}")

class CacheService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            logger.info("Initializing Redis cache...")
            self.provider = RedisCache(redis_url)
        else:
            logger.info("Initializing in-memory cache...")
            self.provider = InMemoryCache()
            
    def _generate_key(self, prefix: str, content: str) -> str:
        h = hashlib.sha256(content.encode()).hexdigest()
        return f"{prefix}:{h}"

    def get_json(self, prefix: str, content: str) -> Optional[Any]:
        key = self._generate_key(prefix, content)
        val = self.provider.get(key)
        if val:
            try:
                return json.loads(val)
            except json.JSONDecodeError:
                return None
        return None

    def set_json(self, prefix: str, content: str, data: Any, ttl: int = 3600):
        key = self._generate_key(prefix, content)
        try:
            val = json.dumps(data)
            self.provider.set(key, val, ttl)
        except TypeError:
            logger.error("Failed to serialize cache data to JSON.")

cache_service = CacheService()
