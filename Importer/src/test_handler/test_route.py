import httpx

from src.settings.loggers.config import log
from src.settings.decorators.logs_decorators import debugs_decorator


class TestRouter:
    def __init__(self, module):
        self.module = module
        self.tester = Tester(self)

    async def process(self, http_method: str, url: str, prefix: str, values: dict):
        response = await self.tester.response_microservice(http_method=http_method, url=url, prefix=prefix, values=values)
        return response

class Tester:
    def __init__(self, router):
        self.router = router

    @debugs_decorator
    async def response_microservice(self, http_method: str, url: str, prefix: str, values: dict):
        async with httpx.AsyncClient() as client:
            try:
                response = await self._make_request(client, http_method=http_method, url=url, prefix=prefix, values=values)
                if response.status_code >= 400:
                        return {
                            "status": False,
                            "response": None
                        }
                return {
                        "status": False,
                        "response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
                    }
        
            except Exception as err:
                log.error('The httpx client error', url=url, error=str(err))
                return {
                    "status": False,
                    "response": None
                }
        
    @debugs_decorator
    async def _make_request(self, client: httpx.AsyncClient, http_method: str, url: str, prefix: str, values: dict):
        if http_method == 'POST':
            if isinstance(values, list):
                values = values[0]
            method = await client.post(url=f"{url}{prefix or ''}", json=values)
        elif http_method == 'GET':
            method = await client.get(url=f"{url}{prefix or ''}", params=values)
        elif http_method == 'UPDATE':
            method = await client.put(url=f"{url}{prefix or ''}", json=values)
        elif http_method == 'DELETE':
            method = await client.delete(url=f"{url}{prefix or ''}", json=values)
        else:
            log.error("Unsupported HTTP method", method=http_method, error=str(ValueError))
            raise
        
        log.info(f"The httpx client sent request to {url}{prefix or ''}", url=url, prefix=prefix)
        return method