from .broker_module import BrokerManager
from src.settings.schemas.models_schemas import RequestDict
from src.settings.get_env_variables import env_variables


class BrokerBridge:
    env_variable = env_variables

    def __init__(self):
        self.manager = BrokerManager(self)

    async def request_importer(self, url: str):
        return await self.manager.request_importer(
            queue_name=self.env_variable.QUEUE_NAME, 
            rmq_url=self.env_variable.RMQ_URL, 
            url=url
        )
    
    async def api_process(self, method: str, request: RequestDict, tag: str, route: str):
        return await self.manager.api_process(
            method=method, 
            request=request, 
            tag=tag, 
            route=route, 
            queue_name=self.env_variable.RPC_NAME, 
            rmq_url=self.env_variable.RMQ_URL, 
            timeout=self.env_variable.TIMEOUT
        )
