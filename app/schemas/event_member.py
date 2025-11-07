from pydantic import BaseModel
from enum import Enum


class MemberStatus(str, Enum):
    joined = "joined"
    pending = "pending"
    rejected = "rejected"


class EventMemberBase(BaseModel):
    user_id: int
    event_id: int
    status: MemberStatus


class EventMemberCreate(EventMemberBase):
    pass


class EventMemberRead(EventMemberBase):
    member_id: int

    class Config:
        from_attributes = True
