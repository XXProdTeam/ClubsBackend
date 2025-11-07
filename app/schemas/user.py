from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    organizer = "organizer"


class UserBase(BaseModel):
    first_name: str
    last_name: str
    role: UserRole


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    user_id: int

    class Config:
        from_attributes = True
