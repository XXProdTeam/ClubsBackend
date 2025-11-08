import enum

from sqlalchemy import Column, Enum, BigInteger, ForeignKey

from sqlalchemy.orm import relationship

from app.db.base import Base


class MemberStatusEnum(enum.Enum):
    ACCEPT = "accept"
    WAIT = "wait"


class EventMember(Base):
    __tablename__ = "event_members"

    member_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    event_id = Column(BigInteger, ForeignKey("events.event_id"), nullable=False)
    status = Column(Enum(MemberStatusEnum), nullable=False)

    user = relationship("User", back_populates="event_members")
    event = relationship("Event", back_populates="members")

    def __repr__(self):
        return f"<EventMember(id={self.member_id}, user_id={self.user_id}, event_id={self.event_id}, status={self.status.value})>"
