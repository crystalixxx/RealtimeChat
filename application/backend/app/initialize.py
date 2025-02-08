from app.database.session import get_db_connection
from app.database.crud.user import create_user
from app.database.schemas.user import UserCreate


def init() -> None:
    connection = next(get_db_connection())

    create_user(
        connection,
        UserCreate(
            username="admin@test.com",
            password="12345678",
            is_superadmin=True,
            is_blocked=False,
        ),
    )


if __name__ == "__main__":
    init()
    print("Superuser created")
