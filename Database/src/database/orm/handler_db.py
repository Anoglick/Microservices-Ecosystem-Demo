from functools import wraps

from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from src.database.models.models import Base, Microservices
from src.settings.loggers.config import log
from src.settings.decorators.logs_decorators import debugs_decorator


class Router:
    def __init__(self, module=None, session=None, engine=None):
        self.module = module

        self.status = False
        self.engine = engine
        self.session = session

    async def process(self, method: str = 'get', tag: str = None, route: str = None, value=None):
        if method == "create":
            manager = await ManagerDataBase(router=self, session=self.session, engine=self.engine).create(tag=tag, value=value)
        if method == "get":
            manager = await ManagerDataBase(self, self.session, engine=self.engine).get(tag=tag)
        if method == "update":
            manager = await ManagerDataBase(self, self.session, engine=self.engine).update(tag=tag, route=route, value=value)
        if method == "delete":
            manager = await ManagerDataBase(self, self.session, engine=self.engine).delete(tag=tag, route=route)

        return manager
    
    @debugs_decorator
    async def _callback(self, **kwargs):
        return await self.module._callback(**kwargs)

def initializa_before_method(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        await self.initialization()
        return await func(self, *args, **kwargs)
    return wrapper


class ManagerDataBase:
    def __init__(self, router, session, engine):
        self.router = router

        self.status = False
        self.session = session
        self.engine = engine

    async def initialization(self):
        if self.status:
            return
        
        if not self.status:
            status = await InitializationDatabase().initialization(engine=self.engine)
            self.status = status

            if not self.status:
                return status

    @debugs_decorator
    @initializa_before_method
    async def create(self, *, tag: str, value: dict):
        try:
            async with self.session as session:
                try:
                    route = Microservices(**value)

                except Exception as err:
                    log.error("Model does not exist", error=str(err), model=Microservices.__name__, tag=tag, method='create')
                    raise

                session.add(route)

                await session.flush()
                await session.commit()

                log.info(f"Created values with tag={tag}", tag=tag)
                
        except Exception as err:
            log.error("Failed session", error=str(err))
            raise

        try:
            message = {
                        "action": "create",
                        "tag": tag,
                        "value": value
                    }
            await self.router._callback(message=message)

        except Exception as err:
            log.error("Callback error", error=str(err))
            raise
    
    @debugs_decorator
    @initializa_before_method
    async def get(self, *, tag = None):
        try:
            async with self.session as session:
                if tag:
                    query = select(Microservices).where(Microservices.tag==tag.lower())
                else:
                    query = select(Microservices)
                
                try:
                    result = await session.execute(query)
                    microservices = result.scalars().all()

                except Exception as err:
                    log.error("Failed to execute query", error=str(err), model=Microservices.__name__, tag=tag, method='get')
                    raise

                if not microservices:
                    log.warning("No microservices found", model=Microservices.__name__, tag=tag)
                    return False

                value = [
                    {
                        "name": microservice.name,
                        "tag": microservice.tag,
                        "route": microservice.route,
                        "method": microservice.method,
                        "microservice_url": microservice.microservice_url,
                        "schema_name": microservice.schema_name,
                        "microservice_schema": microservice.microservice_schema,
                        "test_values": microservice.test_data,
                        "active": microservice.active,
                    }
                    for microservice in microservices
                ]
                    
                return value
            
        except Exception as err:
            log.error("Failed session", error=str(err))
            raise

    @debugs_decorator
    @initializa_before_method
    async def update(self, *, tag: str, route: str, value: dict):
        try:
            async with self.session as session:
                stmt = select(Microservices).where(Microservices.tag==tag, Microservices.route==route)

                try:
                    query = await session.execute(stmt)
                    route_obj = query.scalar_one_or_none()

                except Exception as err:
                    log.error("Failed to execute query", error=str(err), model=Microservices.__name__, tag=tag, method='update')
                    raise

                if not route_obj:
                    return False

                
                for key, item in value.items():
                    try:
                        setattr(route_obj, key, item)

                    except Exception as err:
                        log.warning("Invalid parameters", obj=route_obj, key=key, item=item)

                await session.commit()

        except Exception as err:
            log.error("Failed session", error=str(err))
            raise
    
    @debugs_decorator
    @initializa_before_method
    async def delete(self, *, tag: str, route: str):
        try:
            async with self.session as session:
                stmt = select(Microservices).where(Microservices.tag==tag.lower(), Microservices.route==route)
                
                try:
                    query = await session.execute(stmt)
                    route_obj = query.scalar_one_or_none()

                except Exception as err:
                    log.error("Failed to execute query", error=str(err), model=Microservices.__name__, tag=tag, method='delete')
                    raise

                if not route_obj:
                    return False
                
                await session.delete(route_obj)
                await session.commit()

                message = {
                    "action": "delete",
                    "tag": tag,
                    "route": route
                }
                
                return message

        except Exception as err:
            log.error("Failed session", error=str(err))
            raise


class InitializationDatabase:
    async def initialization(self, engine):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                
                log.info("Database created", DB_NAME=engine.name)
                return True
            
            
        except OperationalError as err:
            if "already exists" in str(err):
                return True
            else:
                log.error("Database does not exist", error=str(err))
                return False

        except Exception as err:
            log.error("Unhandled exception", error=str(err))
            return False