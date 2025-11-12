from pydantic import BaseModel, Field
from datetime import datetime
from app.db.models.user import UserRoleEnum


class EventBase(BaseModel):
    name: str
    description: str | None = None
    place: str | None = None
    start_time: datetime
    end_time: datetime
    image_base64_list: list[str] | None = None
    audience: list[UserRoleEnum]
    member_limit: int = Field(..., ge=1)


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    event_id: int
    num_members: int

    class Config:
        from_attributes = True


class EventMemberResponse(EventRead):
    is_member: bool


class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    place: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    image_base64_list: list[str] | None = None
    audience: list[UserRoleEnum] | None = None
    member_limit: int | None = None
