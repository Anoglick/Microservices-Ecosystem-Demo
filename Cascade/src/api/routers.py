from fastapi import APIRouter, Request
from fastapi.openapi.utils import get_openapi
import httpx

from src.settings.loggers.config import log


class Deleg:
    def __init__(self, app):
        self.app = app

        self.proxy = Proxy()
    
    async def register_dynamic_routes(self, microservices: list):
        for micro in microservices:
            try:
                name = micro["name"]
                tag = micro["tag"]
                route = micro["route"]
                method = micro["method"]
                url = micro["microservice_url"]

                log.info("Registering microservice", microservice_name=name, microservice=micro)

            except Exception as err:
                log.error(f"Invalid microservices parameters", microservice=micro, error=str(err))
                continue
            
            try:
                await self.proxy.create_proxy_route(
                    self.app,
                    name=name,
                    tag=tag,
                    url=f"/{tag.lower()}{route}",
                    method=method,
                    microservice_url=url
                )

            except Exception as err:
                log.error(
                    "Failed to register proxy route",
                    micro_name=micro.get("name"),
                    microservice=micro,
                    error=str(err)
                )
            
        self.app.openapi_schema = None
        get_openapi(
            title="Dynamic Routes API",
            version="1.0.0",
            routes=self.app.routes,
        )

class Proxy:
    async def create_proxy_route(self, app, name: str, tag: str, url: str, method: str, microservice_url: str):
        router = APIRouter()

        async def proxy(request: Request):
            try:
                async with httpx.AsyncClient() as client:
                    forwarded = await client.request(
                        method=method,
                        url=f"{microservice_url}{url}",
                        headers=request.headers.raw,
                        content=await request.body()
                    )
                
                log.info(
                    "Request forwarded", 
                    microservice_name=name,
                    url=f"{microservice_url}{url}", 
                    status=forwarded.status_code
                )
                return forwarded.json()
            
            except Exception as err:
                log.error(
                    "Proxy request failed", 
                    microservice_name=name,
                    url=f"{microservice_url}{url}", 
                    error=str(err)
                )
                raise

        try:
            router.add_api_route(
                path=url,
                endpoint=proxy,
                methods=[method],
                tags=[tag]
            )
            app.include_router(router)

        except Exception as err:
            log.error(
                "The router is't added to the api", 
                microservice_name=name,
                path=url,
                methods=[method],
                tags=[tag],
                error=str(err)
            )
            raise




