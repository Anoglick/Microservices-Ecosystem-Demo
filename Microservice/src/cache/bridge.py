from .cache_manager import CacheManager
from src.settings.databases_setting.settings import rmq_var


class CacheBridge:
    variables = rmq_var

    def __init__(self):
        self.cache_manager = CacheManager(self)

    async def process(self, action: str, *, key: str, value: dict = None):
        cache = await self.cache_manager.process(action=action, key=key, value=value, host=self.variables.HOST, port=self.variables.PORT, db=self.variables.DB, ttl=self.variables.TTL)
        return cache

    async def _callback(self):
        pass