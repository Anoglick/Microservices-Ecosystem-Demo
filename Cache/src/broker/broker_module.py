from .consumer_brokers import ConsumerRouter
from .producer_broker import ProducerRouter


class BrokerManager:
    def __init__(self, bridge):
        self.bridge = bridge
        
        self.consumer_router = ConsumerRouter(self)
        self.producer_router = ProducerRouter(self)
        
    
    async def consumer_process(self, rmq_url: str, queue_name: str):
        await self.consumer_router.consumer_process(rmq_url=rmq_url, queue_name=queue_name)

    async def consumer_callback(self, request):
        await self.bridge.consumer_callback(request)

    async def producer_process(self, message, rmq_url, queue, action):
        return await self.producer_router.producer_process(message=message, rmq_url=rmq_url, queue=queue, action=action)