from .module_manager import ModuleManager


class BridgesHandler:
    def __init__(self):
        self.manager = ModuleManager(self)

    async def process(self, request):
        return await self.manager.process(request)
    