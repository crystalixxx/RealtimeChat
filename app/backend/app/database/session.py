from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.misc.config import config

engine = create_engine(config.PG_CONNECTION_URL)


def get_db_connection() -> Session:
    db = Session(engine)

    try:
        yield db
    finally:
        db.close()
