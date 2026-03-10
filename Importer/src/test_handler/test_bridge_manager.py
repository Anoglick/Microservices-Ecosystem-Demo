from .test_module_manager import TestModuleManager


class TestBridge:
    def __init__(self, manager):
        self.manager = manager
        self.module = TestModuleManager(self)

    async def process(self, http_method: str, url: str, prefix: str = None, values: dict = None):
        return await self.module.process(
            http_method=http_method, 
            url=url, 
            prefix=prefix, 
            values=values
        )