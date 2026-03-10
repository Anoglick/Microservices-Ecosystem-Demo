from .consumer_brokers import ConsumerRouter
from .producer_broker import ProducerRouter


class BrokerManager:
    def __init__(self, bridge, variables):
        self.variables = variables

        self.bridge = bridge
        self.consumer_router = ConsumerRouter(self)
        self.producer_router = ProducerRouter(self)

        
    async def consumer_process(self, rmq_url, queue_names):
        await self.consumer_router.consumer_process(rmq_url=rmq_url, queue_names=queue_names)

    async def consumer_callback(self, message, answer):
        await self.bridge.consumer_callback(message=message, answer=answer)

    async def producer_process(self, action, message):
        if action == 'get' and any(value is not None for key, value in message.items() if key != 'action'):
            await self.producer_router.producer_load(rmq_url=self.variables.RMQ_PRODUCERS_URL, message=message, queue_name=self.variables.PRODUCERS_CACHE_QUEUE)
        else:
            await self.producer_router.producer_save(rmq_url=self.variables.RMQ_PRODUCERS_URL, message=message, queue_name=self.variables.PRODUCERS_DATABASE_QUEUE)
    
    async def producer_response(self, message):
        await self.producer_router.producer_response(rmq_url=self.variables.RMQ_PRODUCERS_URL, message=message)
