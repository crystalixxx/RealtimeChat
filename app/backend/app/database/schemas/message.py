from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    sender_id: int
    chat_id: int
    content: str


class MessageCreate(MessageBase):
    model_config = ConfigDict(from_attributes=True)


class MessageDelete(MessageBase):
    pass


class MessageUpdate(MessageBase):
    model_config = ConfigDict(from_attributes=True)


class Message(MessageBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
