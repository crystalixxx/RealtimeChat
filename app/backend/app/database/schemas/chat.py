from pydantic import BaseModel, ConfigDict


class ChatBase(BaseModel):
    name: str


class ChatCreate(ChatBase):
    model_config = ConfigDict(from_attributes=True)


class ChatDelete(BaseModel):
    pass


class ChatUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Chat(ChatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
