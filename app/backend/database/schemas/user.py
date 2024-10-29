from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str
    is_superuser: bool = False
    is_blocked: bool = False


class UserCreate(UserBase):
    password: str

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
