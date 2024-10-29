from sqlalchemy import create_engine, Session

from app.backend.app.misc.config import config

engine = create_engine(config.PG_CONNECTION_URL)


def get_db_connection() -> Session:
    db = Session(engine)

    try:
        yield db
    finally:
        db.close()
