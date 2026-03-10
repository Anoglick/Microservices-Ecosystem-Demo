from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file="../.env.db", env_file_encoding="utf-8")

class EnvVariables(BaseSettings):
    HOST: str
    PORT: int
    DB: int
    TTL: int | float

    model_config = SettingsConfigDict(env_file="../.env.cache", env_file_encoding="utf-8")

database = DatabaseSettings()
rmq_var = EnvVariables()