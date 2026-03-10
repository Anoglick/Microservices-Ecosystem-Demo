from src.settings.config import env_variables
from src.high_manager import HighManager
from .broker_module import BrokerManager


class BrokerBridge:
    env_variable = env_variables

    def __init__(self):
        self.manager = BrokerManager(self)
        self.high_manager = HighManager(self)

    async def consumer_process(self):
        await self.manager.consumer_process(rmq_url=self.env_variable.RMQ_CONSUMERS_URL, queue_name=self.env_variable.CONSUMERS_QUEUE_NAME)

    async def consumer_callback(self, message):
        await self.high_manager.unpacking(message)

    async def producer_process(self, message, queue_name: str = None):
        await self.manager.producer_process(rmq_url=self.env_variable.RMQ_PRODUCERS_URL, message=message, queue_name=queue_name)
    
    async def producer_reply(self, message, message_reply):
        await self.manager.producer_reply(message=message, message_reply=message_reply)