from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class DataBase:
    def __init__(self):
        self.engine = None
        self.sessionmaker  = None
    
    async def initialize(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
    
        self.sessionmaker  = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def get_session(self):
        if self.sessionmaker  is None:
            raise RuntimeError("Database not initialized")
        async with self.sessionmaker() as session:
            yield session
    