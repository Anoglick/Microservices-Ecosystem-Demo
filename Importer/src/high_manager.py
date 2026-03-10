from src.handlers.bridge_manager import BridgeHandlers


class HighManager:
    def __init__(self):
        self.handlers = BridgeHandlers()

    async def body_handler(self, message, cascade_url):
        await self.handlers.process(url=message, cascade_url=cascade_url)