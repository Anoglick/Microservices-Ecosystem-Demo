from typing import Any, Literal

from pydantic import BaseModel

class RequestDict(BaseModel):
    route: str
    method: Literal['POST', 'GET', 'PUT', 'DELETE']
    tag: str | None = None
    name: str
    schema_name: str
    microservice_schema: dict[str, Any]
    test_data: list[dict[str, Any]]
    microservice_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "route": "/example",
                "method": "GET",
                "tag": "example",
                "name": "microservice_name",
                "schema_name": "Schema",             
                "microservice_schema": {                  
                    "type": "object",
                    "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "descriptions": {"type": "string"},
                    },
                    "required": ["id", "name"]
                },
                "test_data": [
                    {
                        "id": 1
                    },
                    {
                        "id": 2
                    }
                ],
                "microservice_url": "http://localhost:8002"
            }
        }