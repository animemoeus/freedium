from typing import Optional, Any
from upstash_redis import Redis
from app.config import settings
import logging
import threading

logger = logging.getLogger(__name__)

class RedisService:
    _instance: Optional['RedisService'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'RedisService':
        """Ensure only one instance exists (thread-safe singleton)"""
        if cls._instance is None:
            with cls._lock:
                # Double-check locking pattern
                if cls._instance is None:
                    cls._instance = super(RedisService, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'RedisService':
        """Get the singleton instance"""
        return cls()

    def __init__(self):
        # Only initialize once (avoid re-initialization on subsequent calls)
        if not hasattr(self, '_initialized'):
            self._redis: Optional[Redis] = None
            self._connected = False
            self._initialized = True

    def connect(self) -> bool:
        """Initialize Redis connection (lazy initialization)"""
        # If already connected, return True
        if self._connected and self._redis is not None:
            return True

        try:
            if not settings.REDIS_URL or not settings.REDIS_TOKEN:
                logger.warning("Redis URL or token not configured")
                return False

            # Thread-safe connection initialization
            with self._lock:
                # Double-check pattern for connection
                if self._connected and self._redis is not None:
                    return True

                self._redis = Redis(
                    url=settings.REDIS_URL,
                    token=settings.REDIS_TOKEN
                )

                # Test connection
                self._redis.ping()
                self._connected = True
                logger.info("Successfully connected to Redis")
                return True

        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._connected = False
            self._redis = None
            return False

    def disconnect(self) -> None:
        """Disconnect from Redis (thread-safe)"""
        with self._lock:
            if self._redis:
                self._redis = None
                self._connected = False
                logger.info("Disconnected from Redis")

    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        return self._connected and self._redis is not None

    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        if not self.is_connected():
            return None

        try:
            return self._redis.get(key)
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Set value in Redis with optional expiration"""
        if not self.is_connected():
            return False

        try:
            self._redis.set(key, value, ex=ex)
            return True
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        if not self.is_connected():
            return False

        try:
            self._redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists in Redis"""
        if not self.is_connected():
            return False

        try:
            return bool(self._redis.exists(key))
        except Exception as e:
            logger.error(f"Error checking key {key}: {e}")
            return False

    def ping(self) -> bool:
        """Ping Redis to check connection"""
        if not self.is_connected():
            return False

        try:
            self._redis.ping()
            return True
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            return False

# Global Redis service instance
redis_service = RedisService()