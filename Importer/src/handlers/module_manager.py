from .MainHandler import Router


class ModuleManager:
    def __init__(self, bridge):
        self.bridge = bridge
        self.router = Router(self)

    async def process(self, url, cascade_url):
        await self.router.process(url=url, cascade_url=cascade_url)
    
    async def _callback(self, *args, **kwargs):
        return await self.bridge._callback(*args, **kwargs)