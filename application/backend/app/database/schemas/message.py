from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    model_config = ConfigDict(from_attributes=True)


class MessageDelete(MessageBase):
    pass


class MessageUpdate(MessageBase):
    model_config = ConfigDict(from_attributes=True)


class Message(MessageBase):
    sender_id: int
    chat_id: int
    id: int

    model_config = ConfigDict(from_attributes=True)
