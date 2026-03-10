from .general_handler import Router


class ModuleManager:
    def __init__(self, bridge):
        self.bridge = bridge
        self.router = Router(self)

    async def process(self, request):
        preprocessing = await self.router.process(request)
        return preprocessing