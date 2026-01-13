from __future__ import annotations

from yitool.cache.cache import Cache
from yitool.cache.cache_manager import CacheManager, cache_manager
from yitool.cache.memory_cache import MemoryCache
from yitool.cache.redis_cache import RedisCache
from yitool.cache.yi_redis import YiRedis

__all__ = [
    # 缓存基类
    "Cache",
    # 内存缓存
    "MemoryCache",
    # Redis缓存
    "RedisCache",
    # 缓存管理器
    "CacheManager",
    # 全局缓存管理器实例
    "cache_manager",
    # Redis工具类
    "YiRedis"
]
