from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env.db", env_file_encoding="utf-8")

class EnvVariables(BaseSettings):
    RMQ_PRODUCERS_URL: str
    RMQ_CONSUMERS_URL: str

    CONSUMERS_QUEUE_NAME: str
    PRODUCERS_CACHE_QUEUE: str
    PRODUCERS_DATABASE_QUEUE: str

    model_config = SettingsConfigDict(env_file=".env.rmq", env_file_encoding="utf-8")

url = Settings()
env_variables = EnvVariables()