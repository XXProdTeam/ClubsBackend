from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    student = "student"
    applicant = "applicant"


class UserBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    role: UserRole


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    class Config:
        from_attributes = True
