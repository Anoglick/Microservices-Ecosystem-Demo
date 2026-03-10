from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from .models.users_model import Base, Users
from .schemas.user_schema import UsersSchema


class Router:
    def __init__(self, manager, engine, session):
        self.manager = manager
        self.engine = engine
        self.session = session

    async def proccess(self, id: int = None, body: UsersSchema = None, method: str = None):
        if method == 'create':
            return await Warn(self, self.engine, self.session).create(body=body) 
        elif method == 'get':
            return await Warn(self, self.engine, self.session).get(id=id) 
        elif method == 'update':
            return await Warn(self, self.engine, self.session).update(id=id, body=body) 
        elif method == 'delete':
            return await Warn(self, self.engine, self.session).delete(id=id) 
    
    async def _callback(self, name: str, action: str = 'get', *args, **kwargs):
        return await self.manager._callback(name=name, action=action, *args, **kwargs)

def initializa_before_method(func):
    async def wrapper(self, *args, **kwargs):
        await self._initialization()
        return await func(self, *args, **kwargs)
    return wrapper

class InitializationDatabase:
    async def initialization(self, engine):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                return {
                    "status": True
                }
        
        except OperationalError as ex:
            if "already exists" in str(ex):
                return {
                    "status": True
                }
            else:
                return {
                    "status": False,
                    'message': "База данных не существует!",
                    'error': ex
                }

        except Exception as ex:
            return {
                    "status": False,
                    'message': "Неожиданная ошибка",
                    'error': ex
                }

class Warn:
    def __init__(self, router, engine, session):
        self.router = router

        self.status = False
        self.engine = engine
        self.session = session

    async def _initialization(self):
        if self.status:
            return  
        
        if not self.status:
            messages = await InitializationDatabase().initialization(engine=self.engine)
            self.status = messages.get('status', False)

            if not self.status:
                return messages.pop('status', False)

    @initializa_before_method
    async def create(self, body: UsersSchema):
        dict_body = body.model_dump()
        value = Users(**dict_body)
        
        self.session.add(value)
        await self.session.flush()
        new_id = value.id

        await self.router._callback(name='cache', action='create', key=new_id, value=dict_body)
        await self.session.commit()

        return {
            "message": "User created", 
            "id": new_id
        }

    @initializa_before_method
    async def get(self, id):
        answer = await self.router._callback(name='cache', action='get', key=id)
        
        if answer is None:
            query = select(Users).where(Users.id == id)
            request = await self.session.execute(query)
            user_obj = request.scalar_one_or_none()
            await self.session.commit()
            
            if user_obj:
                answer = {column.name: getattr(user_obj, column.name) for column in user_obj.__table__.columns}

            if answer is not None:
                await self.router._callback(name='cache', action='create', key=id, value=answer)
            else:
                return None
            
        return answer

    @initializa_before_method
    async def update(self, id, body):
        stmt = select(Users).where(Users.id==id)
        query = await self.session.execute(stmt)
        user_obj = query.scalar_one_or_none()

        if not user_obj:
            return {
                "status": 404,
                "message": "route not found"
            }

        body = body.model_dump()
        for key, item in body.items():
            setattr(user_obj, key, item)

        await self.session.commit()
        return await self.router._callback(name='cache', action='update', key=id, value=body)

    @initializa_before_method
    async def delete(self, id): 
        stmt = select(Users).where(Users.id==id)
        query = await self.session.execute(stmt)
        user_obj = query.scalar_one_or_none()

        if user_obj:
            user_dict = {column.name: getattr(user_obj, column.name) for column in user_obj.__table__.columns}
        else:
            user_dict = None

        if not user_obj:
            return {
                "status": 404,
                "message": "route not found"
            }
        
        await self.session.delete(user_obj)
        await self.session.commit()

        return await self.router._callback(name='cache', action='delete', key=id, value=user_dict)