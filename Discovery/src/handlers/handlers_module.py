from .request_handler import Router


class HandlersManager:
    def __init__(self, bridge):
        self.router = Router(self)
        self.bridge = bridge
    
    async def process(self, message, answer):
        action, message = await self.router.process(msg=message, answer=answer)
        await self.bridge._callback(action=action, message=message, answer=answer)