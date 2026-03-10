from src.cache.bridge import CacheBridge
from .module_database import ModuleManager
from .schemas.user_schema import UsersSchema


class BridgeDB:
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session
    
    async def process(self, id: int = None, body: UsersSchema = None, method: str = 'get'): 
        return await ModuleManager(self).process(self.engine, self.session, id=id, body=body, method=method)
    
    async def _callback(self, name: str, action: str = 'get', *args, **kwargs):
        if name == 'cache':
            return await CacheBridge().process(action=action, *args, **kwargs)