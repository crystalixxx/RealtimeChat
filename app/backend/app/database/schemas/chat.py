from _datetime import datetime
from pydantic import BaseModel, ConfigDict


class ChatBase(BaseModel):
    name: str


class ChatCreate(ChatBase):
    model_config = ConfigDict(from_attributes=True)


class ChatDelete(ChatBase):
    pass


class ChatUpdate(ChatBase):
    model_config = ConfigDict(from_attributes=True)


class Chat(ChatBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
