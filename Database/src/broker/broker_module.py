from .consumer_brokers import ConsumerRouter
from .producer_broker import ProducerRouter


class BrokerManager:
    def __init__(self, bridge):
        self.consumer_router = ConsumerRouter(self)
        self.producer_router = ProducerRouter(self)
        self.bridge = bridge

        self.channel = None
    
    async def consumer_process(self, rmq_url: str, queue_name: str):
        await self.consumer_router.consumer_process(rmq_url=rmq_url, queue_name=queue_name)

    async def consumer_callback(self, message, channel):
        self.channel = channel
        await self.bridge.consumer_callback(message=message)

    async def producer_process(self, rmq_url: str, message, queue_name: str ):
        await self.producer_router.producer_process(rmq_url=rmq_url, message=message, queue_name=queue_name)
    
    async def producer_reply(self, message, message_reply):
        await self.producer_router.producer_reply(channel=self.channel, message=message, message_reply=message_reply)