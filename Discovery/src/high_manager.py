from src.handlers.handlers_bridge import HandlersBridge


class HighManager:
    def __init__(self, broker):
        self.handlers = HandlersBridge(self)
        self.broker = broker

    async def handles(self, message, answer):
        await self.handlers.process(message=message, answer=answer)

    async def save_data(self, *args, **kwargs):
        await self.broker.consumer_process(*args, **kwargs)

    async def load_data(self, *args, **kwargs):
        await self.broker.producer_process(*args, **kwargs)
    
    async def api_response(self, message):
        await self.broker.producer_response(message=message)

    