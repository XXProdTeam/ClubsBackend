from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Text,
    TIMESTAMP,
    Integer,
)
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import relationship

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    event_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    place = Column(String)
    start_time = Column(TIMESTAMP(timezone=False), nullable=False)
    end_time = Column(TIMESTAMP(timezone=False), nullable=False)
    image_base64_list = Column(JSONB)
    audience = Column(JSONB)
    member_limit = Column(Integer, nullable=True)

    members = relationship("EventMember", back_populates="event")

    def __repr__(self):
        return f"<Event(id={self.event_id}, name={self.name})>"
