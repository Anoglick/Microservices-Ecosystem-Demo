from typing import Any

from pydantic import BaseModel


class UsersSchema(BaseModel):
    username: str
    age: int
    description: str | None = None

class RequestDict(BaseModel):
    route: str
    method: str
    tag: str | None = None
    name: str
    schema_name: str
    microservice_schema: dict[str, Any]
    test_data: list[dict[str, Any]]
    microservice_url: str