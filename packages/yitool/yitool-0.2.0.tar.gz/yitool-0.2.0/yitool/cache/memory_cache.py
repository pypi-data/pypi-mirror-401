from __future__ import annotations

import time
from collections import OrderedDict, deque
from typing import Any

from yitool.cache.cache import Cache

# 尝试导入cachetools库，如果没有安装则使用内置实现
CACHETOOLS_AVAILABLE = False
try:
    from cachetools import FIFOCache, LFUCache, LRUCache, TTLCache
    CACHETOOLS_AVAILABLE = True
except ImportError:
    pass


class MemoryCache(Cache):
    """内存缓存实现，支持多种缓存策略"""

    # 支持的缓存策略
    SUPPORTED_STRATEGIES = ["LRU", "LFU", "FIFO", "TTL"]

    def __init__(self, max_size: int = 1000, strategy: str = "LRU", ttl: int | None = None):
        """初始化内存缓存

        Args:
            max_size: 缓存最大容量
            strategy: 缓存策略，支持 LRU, LFU, FIFO, TTL
            ttl: 过期时间（秒），仅TTL策略有效
        """
        super().__init__()
        self.max_size = max_size
        self.strategy = strategy.upper()
        self.ttl = ttl

        if self.strategy not in MemoryCache.SUPPORTED_STRATEGIES:
            raise ValueError(f"Unsupported strategy: {strategy}. Supported strategies: {', '.join(MemoryCache.SUPPORTED_STRATEGIES)}")

        # 创建缓存实例
        self.cache = self._create_cache()
        # 存储每个键的过期时间
        self.expire_times = {}

    def _create_cache(self):
        """根据策略创建缓存实例

        Returns:
            缓存实例
        """
        if CACHETOOLS_AVAILABLE:
            # 使用cachetools库实现
            if self.strategy == "LRU":
                return LRUCache(maxsize=self.max_size)
            elif self.strategy == "LFU":
                return LFUCache(maxsize=self.max_size)
            elif self.strategy == "FIFO":
                return FIFOCache(maxsize=self.max_size)
            elif self.strategy == "TTL":
                return TTLCache(maxsize=self.max_size, ttl=self.ttl or 3600)
        else:
            # 使用内置实现
            if self.strategy == "LRU":
                return OrderedDict()
            elif self.strategy == "FIFO":
                return deque(maxlen=self.max_size)
            elif self.strategy == "LFU":
                # 简单的LFU实现
                return {}
            elif self.strategy == "TTL":
                return {}

    def _is_expired(self, key: str) -> bool:
        """检查键是否过期

        Args:
            key: 缓存键

        Returns:
            是否过期
        """
        if key not in self.expire_times:
            return False

        expire_time = self.expire_times[key]
        return expire_time is not None and time.time() > expire_time

    def _clean_expired(self):
        """清理过期的键"""
        if self.strategy == "TTL" and not CACHETOOLS_AVAILABLE:
            expired_keys = [key for key in self.cache if self._is_expired(key)]
            for key in expired_keys:
                self.delete(key)

    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存值"""
        self._clean_expired()

        if CACHETOOLS_AVAILABLE:
            value = self.cache.get(key, default)
        else:
            if self.strategy == "LRU":
                if key in self.cache:
                    # 移动到末尾表示最近使用
                    self.cache.move_to_end(key)
                    value = self.cache[key]
                else:
                    value = default
            elif self.strategy == "FIFO":
                value = default
                for item in self.cache:
                    if isinstance(item, tuple) and item[0] == key:
                        value = item[1]
                        break
            elif self.strategy == "LFU":
                value = self.cache.get(key, {}).get("value", default)
            elif self.strategy == "TTL":
                if key in self.cache and not self._is_expired(key):
                    value = self.cache[key]
                else:
                    value = default

        # 触发get事件
        self._emit("get", key, value)
        return value

    def set(self, key: str, value: Any, expire: int | None = None) -> bool:
        """设置缓存值"""
        self._clean_expired()

        if CACHETOOLS_AVAILABLE:
            self.cache[key] = value
        else:
            if self.strategy == "LRU":
                if len(self.cache) >= self.max_size:
                    # 删除最旧的项
                    self.cache.popitem(last=False)
                self.cache[key] = value
                # 移动到末尾表示最近使用
                self.cache.move_to_end(key)
            elif self.strategy == "FIFO":
                if len(self.cache) >= self.max_size:
                    # 删除最旧的项
                    self.cache.popleft()
                self.cache.append((key, value))
            elif self.strategy == "LFU":
                if key in self.cache:
                    # 更新访问次数
                    self.cache[key]["count"] += 1
                    self.cache[key]["value"] = value
                else:
                    if len(self.cache) >= self.max_size:
                        # 删除访问次数最少的项
                        least_used_key = min(self.cache, key=lambda k: self.cache[k]["count"])
                        del self.cache[least_used_key]
                    self.cache[key] = {"value": value, "count": 1}
            elif self.strategy == "TTL":
                self.cache[key] = value
                if expire is not None:
                    self.expire_times[key] = time.time() + expire
                else:
                    self.expire_times[key] = None

        # 触发set事件
        self._emit("set", key, value, expire)
        return True

    def delete(self, key: str) -> bool:
        """删除缓存值"""
        try:
            success = False
            if CACHETOOLS_AVAILABLE:
                if key in self.cache:
                    del self.cache[key]
                    success = True
            else:
                if self.strategy == "LRU":
                    if key in self.cache:
                        del self.cache[key]
                        success = True
                elif self.strategy == "FIFO":
                    # 查找并删除
                    for _i, item in enumerate(self.cache):
                        if isinstance(item, tuple) and item[0] == key:
                            self.cache.remove(item)
                            success = True
                            break
                elif self.strategy == "LFU":
                    if key in self.cache:
                        del self.cache[key]
                        success = True
                elif self.strategy == "TTL":
                    if key in self.cache:
                        del self.cache[key]
                        if key in self.expire_times:
                            del self.expire_times[key]
                        success = True

            if success:
                # 触发delete事件
                self._emit("delete", key)
            return success
        except Exception:
            return False

    def clear(self) -> bool:
        """清空缓存"""
        try:
            if CACHETOOLS_AVAILABLE:
                self.cache.clear()
            else:
                if self.strategy == "LRU":
                    self.cache.clear()
                elif self.strategy == "FIFO":
                    self.cache.clear()
                elif self.strategy == "LFU":
                    self.cache.clear()
                elif self.strategy == "TTL":
                    self.cache.clear()
                    self.expire_times.clear()

            # 触发clear事件
            self._emit("clear")
            return True
        except Exception:
            return False

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        self._clean_expired()

        if CACHETOOLS_AVAILABLE:
            return key in self.cache
        else:
            if self.strategy == "LRU":
                return key in self.cache
            elif self.strategy == "FIFO":
                return any(isinstance(item, tuple) and item[0] == key for item in self.cache)
            elif self.strategy == "LFU":
                return key in self.cache
            elif self.strategy == "TTL":
                return key in self.cache and not self._is_expired(key)

    def incr(self, key: str, delta: int = 1) -> int | None:
        """递增缓存值"""
        self._clean_expired()

        current = self.get(key)
        if current is None:
            current = 0

        if not isinstance(current, (int, float)):
            return None

        new_value = current + delta
        self.set(key, new_value)
        return new_value

    def decr(self, key: str, delta: int = 1) -> int | None:
        """递减缓存值"""
        return self.incr(key, -delta)

    def get_size(self) -> int:
        """获取缓存大小"""
        self._clean_expired()

        if CACHETOOLS_AVAILABLE:
            return len(self.cache)
        else:
            if self.strategy == "LRU":
                return len(self.cache)
            elif self.strategy == "FIFO":
                return len(self.cache)
            elif self.strategy == "LFU":
                return len(self.cache)
            elif self.strategy == "TTL":
                return len(self.cache)
