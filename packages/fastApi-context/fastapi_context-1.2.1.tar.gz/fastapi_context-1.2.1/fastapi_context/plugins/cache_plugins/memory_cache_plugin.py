from dataclasses import dataclass
import time
from typing import Union, Dict, Literal, Optional
from threading import RLock

from fastapi_context.const import CacheBrokerEnum
from fastapi_context.plugins.cache_plugins.base import CacheBroker, CachePluginBase


@dataclass
class CacheEntry:
    value: Union[str, bytes]
    expire_at: Optional[float]


class MemoryCacheBroker(CacheBroker):
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = RLock()

    def _is_expired(self, entry: CacheEntry) -> bool:
        """检查是否过期"""
        return entry.expire_at is not None and entry.expire_at <= time.time()

    def _delete_if_expired(self, key: str) -> bool:
        entry = self._cache.get(key)
        if entry and self._is_expired(entry):
            self._cache.pop(key, None)
            return True
        return False

    def get(self, key: str) -> Optional[Union[str, bytes]]:
        with self._lock:
            # 自动处理过期清理逻辑
            if self._delete_if_expired(key):
                return None
            entry = self._cache.get(key)
            return entry.value if entry else None

    async def async_get(self, key: str) -> Optional[Union[str, bytes]]:
        return self.get(key)

    def set(self, key: str, value: Union[str, bytes], ttl: Optional[int] = None, nx: bool = True) -> bool:
        with self._lock:
            current_entry = self._cache.get(key)

            if nx and current_entry and not self._is_expired(current_entry):
                return False

            expire_at = time.time() + ttl if ttl else None
            self._cache[key] = CacheEntry(value=value, expire_at=expire_at)
            return True

    async def async_set(self, key: str, value: Union[str, bytes], ttl: Optional[int] = None, nx: bool = True) -> bool:
        return self.set(key, value, ttl, nx)

    def delete(self, key: str) -> bool:
        with self._lock:
            return bool(self._cache.pop(key, None))

    async def async_delete(self, key: str) -> bool:
        return self.delete(key)


class MemoryCachePlugin(CachePluginBase):
    type: Literal[CacheBrokerEnum.MEMORY] = CacheBrokerEnum.MEMORY

    def init_cache_broker(self):
        self.broker = MemoryCacheBroker()


__all__ = ["MemoryCachePlugin"]
