from sqlalchemy import (
    Column,
    String,
    BigInteger,
)

from app.db.base import Base

class EventImage(Base):
    __tablename__ = "event_images"

    image_id = Column(BigInteger, primary_key=True, index=True)
    base64_str = Column(String, nullable=False)