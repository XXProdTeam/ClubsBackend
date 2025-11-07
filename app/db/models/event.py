from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Text,
    TIMESTAMP,
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
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    image_id_list = Column(JSONB)
    tag = Column(JSONB)
    audience = Column(JSONB)

    members = relationship("EventMember", back_populates="event")
