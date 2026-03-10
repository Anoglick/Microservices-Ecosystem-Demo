from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvVariables(BaseSettings):
    RMQ_URL: str
    QUEUE_NAME: str
    RPC_NAME: str
    TIMEOUT: int | float

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

env_variables = EnvVariables()