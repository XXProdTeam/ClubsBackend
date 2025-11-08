from app.db.models.event import Event

from app.schemas.event import EventCreate
from app.core.exceptions import get_or_404

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class EventCRUD:
    async def create_event(self, db: AsyncSession, event: EventCreate):
        pass

    async def get_event(self, db: AsyncSession, event_id: int):
        pass

    async def get_events(self, db: AsyncSession):
        pass

    async def delete_event(self, db: AsyncSession, event_id: int):
        pass

    async def update_event(self, db: AsyncSession, event_id: int, event: EventCreate):
        pass

    async def get_event_members(self, db: AsyncSession, event_id: int):
        pass
