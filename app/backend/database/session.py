from sqlalchemy import create_engine, Session

from app.backend.misc.config import config

engine = create_engine(
    config.pg_connection_url()
)


def get_db_connection() -> Session:
    db = Session(engine)

    try:
        yield db
    finally:
        db.close()