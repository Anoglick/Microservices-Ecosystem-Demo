from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

from .routers import Deleg
from src.high_manager import HighManager
from src.settings.schemas.models_schemas import RequestDict
from src.settings.decorators.logs_decorators import debugs_decorator
from src.settings.loggers.config import log


router = APIRouter(prefix="/v1", tags=["urls"])
manager = HighManager()

@router.on_event("startup")
async def on_startup():
    deleg_proxy = Deleg(router)

    try:
        microservices = await manager.api_process(method='get')
    except Exception as err:
        log.error("Failed to fetch microservices on startup", error=str(err))
        return
    
    if isinstance(microservices, list):
        await deleg_proxy.register_dynamic_routes(microservices=microservices)
    else:
        log.error("Invalid response received on startup")


@router.post('/signal')
@debugs_decorator
async def initialize_microservice(url: str):
    result = await manager.pull_signal(url=url)
    return JSONResponse(content=result, status_code=result.get("status", 200))

@router.post('/create')
@debugs_decorator
async def create_route(request: RequestDict):
    await manager.api_process(method='create', request=request.model_dump())
    return {
        "message": "The microservice has been registered",
        "status": 201
    }

@router.get('/get')
@debugs_decorator
async def get_route(tag: str):
    result = await manager.api_process(method='get', tag=tag.upper())
    return JSONResponse(content=result)

@router.put('/update')
@debugs_decorator
async def update_route(request: RequestDict):
    result = await manager.api_process(method='update', request=request.model_dump())
    return JSONResponse(content=result, status_code=result.get("status", 201))

@router.delete('/delete')
@debugs_decorator
async def delete_route(tag: str, route: str):
    result = await manager.api_process(method='delete', tag=tag.upper(), route=route)
    return JSONResponse(content=result, status_code=result.get("status", 200))


app = FastAPI(
    title="Cascade Service",
    openapi_tags=[
        {"name": "v1", "description": "Версия 1 API"}
    ]
)
app.include_router(router)