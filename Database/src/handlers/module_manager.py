from .general_handler import Router


class ModuleManager:
    def __init__(self, bridge):
        self.bridge = bridge

    async def process(self, request):
        preprocessing = await Router(self, request).process()
        return preprocessing