from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


async_engine = create_async_engine(
    "postgresql+asyncpg://postgres:ZZZclash19963@localhost:5432/notes"
)

new_session = async_sessionmaker(async_engine, expire_on_commit=False)
engine = create_async_engine(
    "postgresql+asyncpg://postgres:ZZZclash19963@localhost:5432/notes",
    echo=True,
)