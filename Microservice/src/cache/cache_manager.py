from datetime import timedelta

from .handler import Cachevaluer


class CacheManager:
    def __init__(self, bridge):
        self.bridge = bridge
        self.cache_router = Cachevaluer(self)

    async def process(self, action: str, *, key: str, value: dict, host: str, port: int, db: int, ttl: int | timedelta):
        cache = await self.cache_router.process(action=action, key=key, value=value, host=host, port=port, db=db, ttl=ttl)
        return cache

    async def _callback(self):
        pass