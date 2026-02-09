from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings


async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)

new_session = async_sessionmaker(async_engine, expire_on_commit=False)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)