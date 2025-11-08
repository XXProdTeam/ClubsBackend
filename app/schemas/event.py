from pydantic import BaseModel
from datetime import datetime
from app.db.models.user import UserRoleEnum


class EventBase(BaseModel):
    name: str
    description: str | None = None
    place: str | None = None
    start_time: datetime
    end_time: datetime
    image_base64_list: list[str] | None = None
    audience: list[UserRoleEnum] = None
    member_limit: int


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    event_id: int

    class Config:
        from_attributes = True
