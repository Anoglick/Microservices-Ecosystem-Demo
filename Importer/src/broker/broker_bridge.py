from .broker_module import BrokerManager
from src.high_manager import HighManager
from src.settings.get_env_variables import env_variables


class BrokerBridge:
    env_variable = env_variables

    def __init__(self):
        self.high_manager = HighManager()
        self.module = BrokerManager(self)

    async def consumer_process(self):
        await self.module.consumer_process(
            rmq_url=self.env_variable.RMQ_URL, 
            queue_name=self.env_variable.QUEUE_NAME
        )

    async def consumer_callback(self, message):
        await self.high_manager.body_handler(message, self.env_variable.CASCADE_URL)