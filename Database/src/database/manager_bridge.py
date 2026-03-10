from .module_manager import ModuleManager


class BridgesDB:
    def __init__(self, manager):
        self.manager = manager
        self.db_manager = ModuleManager(self)

    async def process(self, engine, session, method, tag: str = None, route: str = None, value=None):
        response_db = await self.db_manager.process(method=method, engine=engine, session=session, tag=tag, route=route, value=value)
        return response_db

    async def _callback(self, message):
        await self.manager.answer_cache(message=message)