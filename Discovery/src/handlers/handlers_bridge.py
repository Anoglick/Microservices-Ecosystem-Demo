from .handlers_module import HandlersManager


class HandlersBridge:
    def __init__(self, high_manager):
        self.manager = HandlersManager(self)
        self.high_manager = high_manager

    async def process(self, message, answer):
        await self.manager.process(message=message, answer=answer)

    async def _callback(self, action, message, answer):
        if answer:
            await self.high_manager.api_response(message)
        else:
            await self.high_manager.load_data(action, message)