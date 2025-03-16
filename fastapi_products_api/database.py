from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_products_api.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
