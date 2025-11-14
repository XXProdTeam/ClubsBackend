from pydantic import BaseModel
from app.db.models.event_member import MemberStatusEnum


class EventMemberBase(BaseModel):
    user_id: int
    event_id: int
    status: MemberStatusEnum = MemberStatusEnum.WAIT


class EventMemberCreate(EventMemberBase):
    pass


class EventMemberRead(EventMemberBase):
    member_id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True
