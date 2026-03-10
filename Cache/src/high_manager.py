from src.cache.cache_bridge import CacheBridge
from src.handlers.manager_bridge import BridgesHandler


class HighManager:
    def __init__(self, broker):
        self.broker = broker
        self.cache_manager = CacheBridge(self)
        self.handlers_manager = BridgesHandler()

    async def process(self, request):
        answer = await self.handlers_manager.process(request)
        action, key, route, value = answer['action'], answer['key'], answer['route'], answer['value']
        values = await self.cache_manager.process(action=action, key=key, route=route, value=value)
        await self.pull_request(values, action='discovery')
    
    async def pull_request(self, message, action: str = None):
        return await self.broker.producer_process(message=message, action=action)