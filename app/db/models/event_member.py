import enum

from sqlalchemy import (
    Column,
    Enum,
    BigInteger,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.db.base import Base

class MemberStatus(enum.Enum):
    ACCEPTED = "accepted"
    WAITED = "waited"

class EventMember(Base):
    __tablename__ = "event_members"

    member_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    event_id = Column(BigInteger, ForeignKey("events.event_id"), nullable=False)
    status = Column(Enum(MemberStatus), nullable=False)

    user = relationship("User", back_populates="events")
    event = relationship("Event", back_populates="members")