from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class EventBase(BaseModel):
    name: str
    description: str | None = None
    place: str | None = None
    start_time: datetime
    end_time: datetime
    image_id_list: list[int] | None = None
    tag: Optional[Any] = None
    audience: Optional[Any] = None


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    event_id: int

    class Config:
        from_attributes = True
