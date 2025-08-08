from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from bot.core.config import settings

engine = create_async_engine(settings.db_url, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
