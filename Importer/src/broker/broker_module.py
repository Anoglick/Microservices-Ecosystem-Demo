from .consumer_brokers import Router


class BrokerManager:
    def __init__(self, bridge):
        self.router = Router(self)
        self.bridge = bridge

    async def consumer_process(self, rmq_url: str, queue_name: str):
        await self.router.consumer_process(rmq_url=rmq_url, queue_name=queue_name)

    async def consumer_callback(self, message):
        await self.bridge.consumer_callback(message)