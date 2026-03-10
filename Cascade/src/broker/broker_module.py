from src.settings.schemas.models_schemas import RequestDict
from .producer_brokers import ProducerRouter


class BrokerManager:
    def __init__(self, bridge):
        self.bridge = bridge
        self.producer_router = ProducerRouter(self)
    
    async def request_importer(self, queue_name: str, rmq_url: str, url: str):
        return await self.producer_router.request_importer(queue_name=queue_name, rmq_url=rmq_url, url=url)
    
    async def api_process(
            self, 
            method: str, 
            request: RequestDict, 
            tag: str, 
            route: str, 
            queue_name: str, 
            rmq_url: str, 
            timeout: int | float
        ):
        return await self.producer_router.request_discovery(
            method=method, 
            request=request, 
            tag=tag, 
            route=route, 
            queue_name=queue_name, 
            rmq_url=rmq_url, 
            timeout=timeout
        )