from .module_manager import ModuleManager


class BridgesHandler:
    def __init__(self):
        self.module = ModuleManager(self)

    async def process(self, request):
        return await self.module.process(request)