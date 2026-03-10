from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.settings.loggers.config import log


class DataBase:
    def __init__(self):
        self.engine = None
        self.sessionmaker  = None
    
    async def initialize(self, url: str, echo: bool = False):
        try:
            self.engine = create_async_engine(
                url=url,
                echo=echo
            )
            log.info("The database engine has been created", url=url)

        except Exception as err:
            log.error("Failed create the database engine", url=url, error=str(err))
            raise

        try:
            self.sessionmaker = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            log.info("The database sessionmaker has been created")

        except Exception as err:
            log.error("Failed create the database sessionmaker", url=url, error=str(err))
            raise
    
    async def get_session(self):
        try:
            return self.sessionmaker()
        
        except Exception as err:
            log.error("Database not initialized", error=str(err))
            raise