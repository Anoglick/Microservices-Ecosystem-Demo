from src.settings.config import env_variables
from src.high_manager import HighManager
from .broker_module import BrokerManager


class BrokerBridge:
    env_variable = env_variables

    def __init__(self):
        self.manager = BrokerManager(bridge=self, variables=self.env_variable)
        self.high_manager = HighManager(self)

    async def consumer_process(self):
        await self.manager.consumer_process(
            rmq_url=self.env_variable.RMQ_CONSUMERS_URL, 
            queue_names=self.env_variable.CONSUMERS_QUEUE_NAMES
        )

    async def consumer_callback(self, message, answer):
        await self.high_manager.handles(message=message, answer=answer)

    async def producer_process(self, action, message):
        await self.manager.producer_process(action, message)
    
    async def producer_response(self, message):
        await self.manager.producer_response(message=message)