from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvVariables(BaseSettings):
    RMQ_PRODUCERS_URL: str
    RMQ_CONSUMERS_URL: str

    CONSUMERS_QUEUE_NAMES: str
    PRODUCERS_CACHE_QUEUE: str
    PRODUCERS_DATABASE_QUEUE: str

    @field_validator("CONSUMERS_QUEUE_NAMES", mode="after")
    def split_consumers(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

env_variables = EnvVariables()