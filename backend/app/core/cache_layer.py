import hashlib
import time
import logging
import os

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)

class GlobalCache:
    """A caching layer utilizing Redis for production, falling back to in-memory for MVP."""
    def __init__(self, ttl_seconds: int = 86400):
        # 86400 seconds = 24 hours
        self.ttl = ttl_seconds
        
        # Try to connect to Redis if the package is installed
        self.use_redis = False
        if REDIS_AVAILABLE:
            redis_host = os.environ.get("REDIS_HOST", "localhost")
            redis_port = int(os.environ.get("REDIS_PORT", 6379))
            try:
                self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, socket_timeout=1)
                self.redis_client.ping()
                self.use_redis = True
                logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
            except Exception as e:
                logger.warning(f"Redis unavailable, falling back to in-memory cache. Error: {e}")
                
        self._memory_cache = {}

    def _generate_key(self, content: str) -> str:
        """Generates a fast MD5 hash key for the given string content."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def get(self, content: str):
        key = self._generate_key(content)
        
        # 1. Try Redis
        if self.use_redis:
            try:
                import json
                cached_data = self.redis_client.get(key)
                if cached_data:
                    logger.info(f"Redis Cache HIT for key: {key[:8]}...")
                    return json.loads(cached_data)
            except Exception as e:
                logger.error(f"Redis GET failed: {e}")
                
        # 2. Try In-Memory Fallback
        if key in self._memory_cache:
            entry = self._memory_cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                logger.info(f"Memory Cache HIT for key: {key[:8]}...")
                return entry['data']
            else:
                logger.info(f"Memory Cache EXPIRED for key: {key[:8]}...")
                del self._memory_cache[key]
                
        return None

    def set(self, content: str, data: dict):
        key = self._generate_key(content)
        
        # 1. Try Redis
        if self.use_redis:
            try:
                import json
                self.redis_client.setex(key, self.ttl, json.dumps(data))
                logger.info(f"Redis Cache SET for key: {key[:8]}...")
                return
            except Exception as e:
                logger.error(f"Redis SET failed: {e}")
                
        # 2. Fallback In-Memory
        self._memory_cache[key] = {
            'timestamp': time.time(),
            'data': data
        }
        logger.info(f"Memory Cache SET for key: {key[:8]}...")

# Singleton instance
cache = GlobalCache()
