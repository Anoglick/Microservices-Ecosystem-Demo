from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session

from src.high_manager import HighManager
from src.high_manager import Importer
from src.database.schemas.user_schema import UsersSchema, RequestDict


router = APIRouter(prefix="/users", tags=["v1"])
importer = Importer()
manager = HighManager()

@router.on_event("startup")
async def on_startup():
    await importer.manage()
    manager.engine = importer.engine

@router.post('/register-microservice')
async def register_microservice():
    return RequestDict(
        name='users_test',
        route='/create',
        method='POST',
        tag='users',
        schema_name="RequestDict",
        microservice_schema={
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "age": {"type": "integer"},
                "description": {"type": "string"}
            },
            "required": ["username", "age"]
        },
        test_data=[
            {
                "username": "John",
                "age": 15
            },
            {
                "username": "Anthony",
                "age": 20,
                "description": "My life doesn't exist"
            },
            {
                "username": "Stark",
                "age": 40
            }
        ],
        microservice_url="http://microservice:8002"
    )

@router.post('/create')
async def user_create(body: UsersSchema, session: Session = Depends(importer.get_session)):
    return await manager.process(session=session, body=body, method='create')

@router.get('/get-user/{id}')
async def user_get(id: int, session: Session = Depends(importer.get_session)):
    return await manager.process(session=session, id=id, method='get')

@router.put('/update-user/{id}')
async def user_update(id: int, body: UsersSchema, session: Session = Depends(importer.get_session)):
    return await manager.process(session=session, id=id, body=body, method='update')

@router.delete('/delete-user/{id}')
async def user_delete(id: int, session: Session = Depends(importer.get_session)):
    return await manager.process(session=session, id=id, method='delete')

app = FastAPI(
    title="Users Service",
    openapi_tags=[
        {"name": "v1", "description": "Версия 1 API"}
    ]
)
app.include_router(router)