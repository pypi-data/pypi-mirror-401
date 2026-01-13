from __future__ import annotations

import json
from typing import Any

from yitool.cache.cache import Cache
from yitool.log import logger

# 尝试导入redis库，如果没有安装则使用try-except
REDIS_AVAILABLE = False
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    pass


class RedisCache(Cache):
    """Redis分布式缓存实现"""

    def __init__(self, redis_client: redis.Redis | None = None, prefix: str = "yitool:", host: str = "localhost", port: int = 6379, db: int = 0, password: str | None = None):
        """初始化Redis缓存

        Args:
            redis_client: 已有的Redis客户端实例，如果为None则创建新实例
            prefix: 缓存键前缀，用于区分不同应用
            host: Redis主机地址
            port: Redis端口
            db: Redis数据库索引
            password: Redis密码
        """
        super().__init__()
        if not REDIS_AVAILABLE:
            raise ImportError("redis library is not installed. Please install it with: pip install redis")

        self.prefix = prefix
        self.redis_client = redis_client or self._create_redis_client(host, port, db, password)

    def _create_redis_client(self, host: str, port: int, db: int, password: str | None) -> redis.Redis:
        """创建Redis客户端

        Args:
            host: Redis主机地址
            port: Redis端口
            db: Redis数据库索引
            password: Redis密码

        Returns:
            Redis客户端实例
        """
        try:
            client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True
            )
            # 测试连接
            client.ping()
            return client
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    def _get_full_key(self, key: str) -> str:
        """获取带前缀的完整键

        Args:
            key: 原始键

        Returns:
            带前缀的完整键
        """
        return f"{self.prefix}{key}"

    def _serialize_value(self, value: Any) -> str:
        """序列化值

        Args:
            value: 要序列化的值

        Returns:
            序列化后的字符串
        """
        return json.dumps(value, ensure_ascii=False)

    def _deserialize_value(self, value: str) -> Any:
        """反序列化值

        Args:
            value: 要反序列化的字符串

        Returns:
            反序列化后的对象
        """
        return json.loads(value)

    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存值"""
        full_key = self._get_full_key(key)
        try:
            value = self.redis_client.get(full_key)
            if value is None:
                value = default
            else:
                value = self._deserialize_value(value)
            # 触发get事件
            self._emit("get", key, value)
            return value
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            # 触发get事件
            self._emit("get", key, default)
            return default

    def set(self, key: str, value: Any, expire: int | None = None) -> bool:
        """设置缓存值"""
        full_key = self._get_full_key(key)
        try:
            serialized_value = self._serialize_value(value)
            if expire is None:
                result = self.redis_client.set(full_key, serialized_value)
            else:
                result = self.redis_client.setex(full_key, expire, serialized_value)
            success = result is True
            # 触发set事件
            if success:
                self._emit("set", key, value, expire)
            return success
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """删除缓存值"""
        full_key = self._get_full_key(key)
        try:
            result = self.redis_client.delete(full_key)
            success = result > 0
            # 触发delete事件
            if success:
                self._emit("delete", key)
            return success
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False

    def clear(self) -> bool:
        """清空缓存"""
        try:
            # 使用SCAN命令查找所有匹配前缀的键
            keys = []
            cursor = 0
            while True:
                cursor, batch = self.redis_client.scan(cursor=cursor, match=f"{self.prefix}*")
                keys.extend(batch)
                if cursor == 0:
                    break

            if keys:
                self.redis_client.delete(*keys)
            # 触发clear事件
            self._emit("clear")
            return True
        except Exception as e:
            logger.error(f"Redis clear error: {e}")
            return False

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        full_key = self._get_full_key(key)
        try:
            result = self.redis_client.exists(full_key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False

    def incr(self, key: str, delta: int = 1) -> int | None:
        """递增缓存值"""
        full_key = self._get_full_key(key)
        try:
            if delta == 1:
                return self.redis_client.incr(full_key)
            else:
                return self.redis_client.incrby(full_key, delta)
        except Exception as e:
            logger.error(f"Redis incr error: {e}")
            return None

    def decr(self, key: str, delta: int = 1) -> int | None:
        """递减缓存值"""
        full_key = self._get_full_key(key)
        try:
            if delta == 1:
                return self.redis_client.decr(full_key)
            else:
                return self.redis_client.decrby(full_key, delta)
        except Exception as e:
            logger.error(f"Redis decr error: {e}")
            return None

    def get_size(self) -> int:
        """获取缓存大小"""
        try:
            # 使用SCAN命令统计匹配前缀的键数量
            count = 0
            cursor = 0
            while True:
                cursor, batch = self.redis_client.scan(cursor=cursor, match=f"{self.prefix}*")
                count += len(batch)
                if cursor == 0:
                    break
            return count
        except Exception as e:
            logger.error(f"Redis get_size error: {e}")
            return 0

    def hget(self, key: str, field: str, default: Any = None) -> Any:
        """获取哈希表字段值

        Args:
            key: 缓存键
            field: 哈希表字段
            default: 默认值

        Returns:
            哈希表字段值或默认值
        """
        full_key = self._get_full_key(key)
        try:
            value = self.redis_client.hget(full_key, field)
            if value is None:
                return default
            return self._deserialize_value(value)
        except Exception as e:
            logger.error(f"Redis hget error: {e}")
            return default

    def hset(self, key: str, field: str, value: Any) -> bool:
        """设置哈希表字段值

        Args:
            key: 缓存键
            field: 哈希表字段
            value: 字段值

        Returns:
            是否设置成功
        """
        full_key = self._get_full_key(key)
        try:
            serialized_value = self._serialize_value(value)
            result = self.redis_client.hset(full_key, field, serialized_value)
            return result > 0
        except Exception as e:
            logger.error(f"Redis hset error: {e}")
            return False

    def hdel(self, key: str, field: str) -> bool:
        """删除哈希表字段

        Args:
            key: 缓存键
            field: 哈希表字段

        Returns:
            是否删除成功
        """
        full_key = self._get_full_key(key)
        try:
            result = self.redis_client.hdel(full_key, field)
            return result > 0
        except Exception as e:
            logger.error(f"Redis hdel error: {e}")
            return False

    def hgetall(self, key: str) -> dict[str, Any]:
        """获取哈希表所有字段值

        Args:
            key: 缓存键

        Returns:
            哈希表所有字段值
        """
        full_key = self._get_full_key(key)
        try:
            result = self.redis_client.hgetall(full_key)
            return {field: self._deserialize_value(value) for field, value in result.items()}
        except Exception as e:
            logger.error(f"Redis hgetall error: {e}")
            return {}
