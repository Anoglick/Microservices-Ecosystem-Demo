from .module_manager import ModuleManager
from src.test_handler.test_bridge_manager import TestBridge
from src.settings.loggers.config import log


class BridgeHandlers:
    def __init__(self):
        self.manager = ModuleManager(self)
        self.test = TestBridge(self)

    async def process(self, url, cascade_url):
        await self.manager.process(url=url, cascade_url=cascade_url)
    
    async def _callback(self, *args, **kwargs):
        try:
            log.info('Calling the test module', args=args, kwargs=kwargs)
            return await self.test.process(*args, **kwargs)
        
        except Exception as err:
            log.error('The test module returned an error', args=args, kwargs=kwargs, error=str(err))
            raise