from .database.manager_bridge import BridgeDB
from .settings.databases_setting.settings import database
from .settings.databases_setting.customization import DataBase


class Importer:
    def __init__(self):
        self.url = database.ASYNC_DATABASE_URL

        self.database = DataBase()
        self.engine = None
    
    async def manage(self):
        await self.database.initialize(self.url)
        self.engine = self.database.engine

    async def get_session(self):
        async for session in self.database.get_session():
            yield session

class HighManager:
    def __init__(self):
        self.engine = None
    
    async def process(self, session, *args, **kwargs):
        return await BridgeDB(engine=self.engine, session=session).process(*args, **kwargs)