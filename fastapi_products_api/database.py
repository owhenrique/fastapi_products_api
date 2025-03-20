from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_products_api.settings import Settings

settings = Settings()
engine = create_async_engine(settings.DATABASE_URL)


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
