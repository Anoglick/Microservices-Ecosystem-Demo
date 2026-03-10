from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvVariables(BaseSettings):
    RMQ_PRODUCERS_URL: str
    RMQ_CONSUMERS_URL: str

    CONSUMERS_QUEUE_NAME: str
    PRODUCERS_CACHE_QUEUE: str
    PRODUCERS_DATABASE_QUEUE: str

    HOST: str
    PORT: int
    DB: int
    TTL: int | float

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

env_variables = EnvVariables()