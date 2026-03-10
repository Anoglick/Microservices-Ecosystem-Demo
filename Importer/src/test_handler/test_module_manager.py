from .test_route import TestRouter


class TestModuleManager:
    def __init__(self, bridge):
        self.bridge = bridge
        self.router = TestRouter(self)

    async def process(self, http_method: str, url: str, prefix: str, values: dict):
        return await self.router.process(
            http_method=http_method, 
            url=url, 
            prefix=prefix, 
            values=values
        )