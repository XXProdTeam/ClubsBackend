import enum

from sqlalchemy import (
    Column,
    Enum,
    String,
    BigInteger,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    APPLICANT = "applicant"


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    event_members = relationship("EventMember", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.user_id}, name={self.first_name} {self.last_name}, role={self.role.value})>"
