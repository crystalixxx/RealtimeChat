from core.interfaces import AbstractUnitOfWork
from database.schemas.user import User, UserCreate, UserUpdate
from misc.security import get_hashed_password


class UserService:
    async def get_user_by_id(self, uow: AbstractUnitOfWork, user_id: int) -> User | None:
        async with uow as session:
            user = await session.users.find_one({"id": user_id})
            return user

    async def get_all_users(self, uow: AbstractUnitOfWork) -> list[User] | None:
        async with uow as session:
            users = await session.users.find_all()
            return users

    async def get_user_by_username(self, uow: AbstractUnitOfWork, username: str) -> User | None:
        async with uow as session:
            user = await session.users.find_one({"username": username})
            return user

    async def get_common_users(self, uow: AbstractUnitOfWork, user_id: int) -> list[User] | None:
        async with uow as session:
            users = await session.users.find_some({"is_superadmin": False})
            users = [user for user in users if user.id != user_id]

            return users

    async def create_user(self, uow: AbstractUnitOfWork, user: UserCreate) -> int | None:
        existing_user = await self.get_user_by_username(uow, user.username)
        if existing_user is not None:
            return None

        hashed_password = get_hashed_password(user.password)

        user_dict = user.model_dump(exclude_none=True)
        user_dict["hashed_password"] = hashed_password
        del user_dict["password"]

        with uow as session:
            user_id = await session.users.add_one(user_dict)
            return user_id

    async def delete_user(self, uow: AbstractUnitOfWork, user_id: int) -> User | None:
        existing_user = await self.get_user_by_id(uow, user_id)
        if not existing_user:
            return None

        with uow as session:
            user = await session.users.delete({"id": user_id})
            return user

    async def update_user(self, uow: AbstractUnitOfWork, user_id: int, user: UserUpdate) -> User | None:
        existing_user = await self.get_user_by_id(uow, user_id)
        if not existing_user:
            return None

        user_dict = user.model_dump(exclude_none=True)

        if "password" in user_dict:
            setattr(user_dict, "hashed_password", get_hashed_password(user_dict["password"]))
            del user_dict["password"]

        with uow as session:
            user = await session.users.update_one({"id": user_id}, user_dict)
            return user

    async def block_user(self, uow: AbstractUnitOfWork, user_id: int) -> User | None:
        existing_user = await self.get_user_by_id(uow, user_id)
        if not existing_user:
            return None

        if existing_user.is_blocked or existing_user.is_superadmin:
            return None

        with uow as session:
            user = await session.users.update_one({"id": user_id}, {"is_blocked": True})
            return user

    async def unblock_user(self, uow: AbstractUnitOfWork, user_id: int) -> User | None:
        existing_user = await self.get_user_by_id(uow, user_id)
        if not existing_user:
            return None

        if not existing_user.is_blocked:
            return None

        with uow as session:
            user = await session.users.update_one({"id": user_id}, {"is_blocked": False})
            return user
