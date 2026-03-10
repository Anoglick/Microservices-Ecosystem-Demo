from datetime import timedelta

from .handler import Router


class Module:
    def __init__(self, bridge):
        self.bridge = bridge

    async def process(self, action: str, *, key: str, route: str = None, value: dict = None, host: str, port: int, db: int = 0, ttl: int | timedelta = 600):
        cache = await Router(self).process(action=action, key=key, route=route, value=value, host=host, port=port, db=db, ttl=ttl)
        return cache
    
    async def _callback(self, message, action: str = None):
        return await self.bridge._callback(message=message, action=action)


