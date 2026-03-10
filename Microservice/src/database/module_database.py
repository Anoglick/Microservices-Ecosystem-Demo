from sqlalchemy.ext.asyncio import AsyncSession

from .actions import Router
from .schemas.user_schema import UsersSchema


class ModuleManager:
    def __init__(self, bridge):
        self.bridge = bridge

    async def process(self, engine, session: AsyncSession, id: int = None, body: UsersSchema = None, method: str = 'get'):
        return await Router(manager=self, engine=engine, session=session).proccess(id=id, body=body, method=method)
    
    async def _callback(self, name: str, action: str = 'get', *args, **kwargs):
        return await self.bridge._callback(name=name, action=action, *args, **kwargs)