from pydantic import BaseModel


class EventImageBase(BaseModel):
    base64_str: str


class EventImageCreate(EventImageBase):
    pass


class EventImageRead(EventImageBase):
    image_id: int

    class Config:
        from_attributes = True
