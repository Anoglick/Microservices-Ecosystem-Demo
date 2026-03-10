from src.settings.schemas.models_schemas import RequestDict
from src.broker.broker_bridge import BrokerBridge
from src.settings.loggers.config import log


class HighManager:
    def __init__(self):
        self.broker = BrokerBridge()
    
    async def pull_signal(self, url: str):
        try:
            result = await self.broker.request_importer(url)
        
        except Exception as err:
            log.error("Microservice request failed", error=str(err))
            return {
                "message": "Microservice unavailable",
                "status": 500
            }
        
        if not result:
            log.warning("Response is empty")
            return {
                "message": "Invalid response", 
                "status": 500
            }

        return result

    async def api_process(self, method: str, request: RequestDict = None, tag: str = None, route: str = None):
        try:
            result = await self.broker.api_process(method=method, request=request, tag=tag, route=route)
        
        except Exception as err:
            log.error("RPC call timed out", error=str(err))
            return {
                "message": "Timed out",
                "status": 500
            }
        
        if not result:
            log.warning("RPC returned empty response")
            result = {
                "message": "Invalid response", 
                "status": 500
            }

        return result