from src.settings.config import env_variables
from .module_manager import Module


class CacheBridge:
    variables = env_variables

    def __init__(self, manager):
        self.manager = manager
        self.module = Module(self)
    
    async def process(self, action: str, *, key: str, route: str = None, value: dict = None):
        cache = await self.module.process(action=action, key=key, route=route, value=value, host=self.variables.HOST, port=self.variables.PORT, db=self.variables.DB, ttl=self.variables.TTL)
        return cache
    
    async def _callback(self, message, action: str = None):
        return await self.manager.pull_request(message=message, action=action)