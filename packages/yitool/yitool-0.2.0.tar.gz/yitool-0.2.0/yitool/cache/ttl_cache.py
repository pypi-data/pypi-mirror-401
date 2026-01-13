from __future__ import annotations

import json
import threading
from typing import Any, Generic, TypeVar

import cachetools

from yitool.cache.yi_redis import YiRedis
from yitool.log import logger

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

class TTLCache(cachetools.TTLCache, Generic[_KT, _VT]):
    """带过期时间的缓存类，支持本地内存缓存和Redis持久化"""

    def __init__(self, maxsize: int, ttl: int, name: str, redis: YiRedis | None = None):
        """初始化缓存

        Args:
            maxsize: 缓存最大容量
            ttl: 缓存过期时间（秒）
            name: 缓存名称，用于Redis键前缀
            redis: YiRedis实例，用于持久化缓存
        """
        super().__init__(maxsize, ttl)
        self._name = name
        self._redis = redis
        self._lock = threading.RLock()  # 添加锁以支持线程安全

        # 初始化时从Redis加载已有数据
        if self.has_redis:
            try:
                self._load_from_redis()
            except Exception as e:
                logger.error(f"Failed to load cache from Redis: {e}")

    @property
    def name(self) -> str:
        return self._name

    @property
    def has_redis(self) -> bool:
        return self._redis is not None and isinstance(self._redis, YiRedis)

    def _redis_key(self, key: _KT) -> str:
        """生成Redis中的键名"""
        return f"{self.name}:{key}"

    def _serialize_value(self, value: _VT) -> Any:
        """序列化值以便存储到Redis"""
        try:
            # 尝试JSON序列化复杂对象
            if isinstance(value, (dict, list, tuple)):
                return json.dumps(value)
            return value
        except (TypeError, ValueError):
            logger.warning(f"Failed to serialize value: {value}")
            return str(value)

    def _deserialize_value(self, value: Any) -> _VT:
        """反序列化Redis中的值"""
        if isinstance(value, bytes):
            value = value.decode("utf-8")

        try:
            # 尝试JSON反序列化
            if isinstance(value, str) and (value.startswith("{") or value.startswith("[")):
                return json.loads(value)
            return value
        except (json.JSONDecodeError, TypeError):
            return value

    def _load_from_redis(self) -> None:
        """从Redis加载缓存数据"""
        if not self.has_redis:
            return

        pattern = f"{self.name}:*"
        cursor = 0
        while True:
            cursor, keys = self._redis.scan(cursor=cursor, match=pattern)
            for key in keys:
                # 移除前缀以获取原始键
                try:
                    original_key = key.decode("utf-8").replace(f"{self.name}:", "", 1)
                    value = self._redis.get(key)
                    if value is not None:
                        with self._lock:
                            super().__setitem__(original_key, self._deserialize_value(value))
                except Exception as e:
                    logger.error(f"Failed to load key {key} from Redis: {e}")

            if cursor == 0:
                break

    def __setitem__(self, key: _KT, value: _VT) -> None:
        with self._lock:
            super().__setitem__(key, value)

            if self.has_redis:
                try:
                    redis_key = self._redis_key(key)
                    serialized_value = self._serialize_value(value)
                    self._redis.set(redis_key, serialized_value, ex=self.ttl)
                except Exception as e:
                    logger.error(f"Failed to set cache to Redis for key {key}: {e}")

    def __getitem__(self, key: _KT) -> _VT:
        with self._lock:
            try:
                # 首先尝试从本地缓存获取
                return super().__getitem__(key)
            except KeyError:
                # 本地缓存不存在，尝试从Redis获取
                if self.has_redis:
                    try:
                        redis_key = self._redis_key(key)
                        value = self._redis.get(redis_key)
                        if value is not None:
                            deserialized_value = self._deserialize_value(value)
                            # 将Redis中的值加载到本地缓存
                            super().__setitem__(key, deserialized_value)
                            return deserialized_value
                    except Exception as e:
                        logger.error(f"Failed to get cache from Redis for key {key}: {e}")

                # 都不存在，抛出KeyError
                raise

    def __delitem__(self, key: _KT) -> None:
        with self._lock:
            super().__delitem__(key)

            if self.has_redis:
                try:
                    redis_key = self._redis_key(key)
                    self._redis.delete(redis_key)
                except Exception as e:
                    logger.error(f"Failed to delete cache from Redis for key {key}: {e}")

    def __contains__(self, key: object) -> bool:
        with self._lock:
            # 先检查本地缓存
            if super().__contains__(key):
                return True

            # 本地缓存不存在，检查Redis
            if self.has_redis:
                try:
                    redis_key = self._redis_key(key)
                    return self._redis.exists(redis_key)
                except Exception as e:
                    logger.error(f"Failed to check cache existence in Redis for key {key}: {e}")
                    return False

            return False

    def get(self, key: _KT, default: Any | None = None) -> Any | None:
        """获取缓存值，如果不存在则返回默认值"""
        with self._lock:
            try:
                return self.__getitem__(key)
            except KeyError:
                return default

    def clear(self) -> None:
        """清空所有缓存"""
        with self._lock:
            super().clear()

            if self.has_redis:
                try:
                    pattern = f"{self.name}:*"
                    self._redis.clear(pattern)
                except Exception as e:
                    logger.error(f"Failed to clear cache in Redis: {e}")
