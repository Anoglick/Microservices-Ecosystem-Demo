from .orm.handler_db import Router


class ModuleManager:
    def __init__(self, bridge):
        self.bridge = bridge

    async def process(self, engine, session, method, tag: str = None, route: str = None, value=None):
        response_db = await Router(module=self, session=session, engine=engine).process(method=method, tag=tag, route=route, value=value)
        return response_db

    async def _callback(self, message):
        return await self.bridge._callback(message=message)