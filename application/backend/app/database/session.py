from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.misc.config import settings

engine = create_engine(settings.PG_CONNECTION_URL)


def get_db_connection() -> Session:
    db = Session(engine)

    try:
        yield db
    finally:
        db.close()
