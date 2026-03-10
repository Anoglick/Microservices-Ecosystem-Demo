from src.high_manager import HighManager
from src.settings.config import env_variables
from .broker_module import BrokerManager


class BrokerBridge:
    env_variable = env_variables

    def __init__(self):
        self.manager = BrokerManager(self)
        self.high_manager = HighManager(self)

    async def consumer_process(self):
        await self.manager.consumer_process(
            rmq_url=self.env_variable.RMQ_CONSUMERS_URL, 
            queue_name=self.env_variable.CONSUMERS_QUEUE_NAME
        )

    async def consumer_callback(self, request):
        await self.high_manager.process(request)

    async def producer_process(self, message, action = None):
        return await self.manager.producer_process(
            message=message, 
            rmq_url=self.env_variable.RMQ_PRODUCERS_URL, 
            queue=self.env_variable,
            action=action
        )