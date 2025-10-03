from typing import Optional, Any
from upstash_redis import Redis
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self):
        self._redis: Optional[Redis] = None
        self._connected = False

    def connect(self) -> bool:
        """Initialize Redis connection"""
        try:
            if not settings.REDIS_URL or not settings.REDIS_TOKEN:
                logger.warning("Redis URL or token not configured")
                return False

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
            return False

    def disconnect(self) -> None:
        """Disconnect from Redis"""
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