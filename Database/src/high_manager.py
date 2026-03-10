from src.settings.config import url, env_variables
from src.handlers.manager_bridge import BridgesHandler
from src.database.engines_config.settings import DataBase
from src.database.manager_bridge import BridgesDB


class HighManager:
    env_variable = env_variables

    def __init__(self, broker):
        self.handler = BridgesHandler()
        self.db = BridgesDB(self)
        self.database = DataBase()
        self.broker = broker

        self.url = url.ASYNC_DATABASE_URL
        self.engine = None
        self.session = None

        self.message_reply = None

    async def initialization(self):
        await self.database.initialize(self.url)
        self.engine = self.database.engine
        self.session = await self.database.get_session()

    async def unpacking(self, *args, **kwargs):
        answer = await self.handler.process(*args, **kwargs)
        method, tag, route, value, rpc = answer['action'], answer['tag'], answer['route'], answer['value'], answer['rpc']
        await self.initialization()
        database_message = await self.db.process(engine=self.engine, session=self.session, method=method, tag=tag, route=route, value=value)

        if rpc:
            self.message_reply = answer['message']
            await self.answer_cache(message=database_message)
        
        if method == 'delete':
            await self.broker.producer_process(message=database_message, queue_name=self.env_variable.PRODUCERS_CACHE_QUEUE)

        if method == 'get' and tag is None:
            await self.broker.producer_process(message=database_message, queue_name=self.env_variable.PRODUCERS_DATABASE_QUEUE)


    async def cache_processing(self, *args, **kwargs):
        await self.handler.cache(*args, **kwargs)

    async def answer_cache(self, message):
        if self.message_reply is not None:
            await self.broker.producer_reply(message=message, message_reply=self.message_reply)    
        else:
            await self.broker.producer_process(message=message, queue_name=self.env_variable.PRODUCERS_CACHE_QUEUE)