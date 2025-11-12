from app.db.models.event import Event

from app.schemas.event import EventCreate, EventUpdate
from app.core.exceptions import get_or_404
from app.crud.user import UserCRUD

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from zoneinfo import ZoneInfo

class EventCRUD:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.utc_tz = ZoneInfo("UTC")

    async def create_event(self, db: AsyncSession, event: EventCreate) -> Event:
        event.start_time = event.start_time.replace(tzinfo=None)
        event.end_time = event.end_time.replace(tzinfo=None)
        new_event = Event(**event.model_dump(exclude_unset=True))
        db.add(new_event)
        await db.commit()
        await db.refresh(new_event)
        return new_event

    async def get_all_events_for_user(
        self, db: AsyncSession, user_id: int
    ) -> list[Event]:
        user = await self.user_crud.get_user_by_id(db, user_id)
        events = select(Event).where(Event.audience.contains([user.role]))
        result = await db.execute(events)
        return get_or_404(
            result.scalars().all(), detail="No events found for this user"
        )

    async def get_all_events(self, db: AsyncSession) -> list[Event]:
        events = select(Event)
        result = await db.execute(events)
        return get_or_404(result.scalars().all(), detail="No events found")

    async def get_event_by_id(self, db: AsyncSession, event_id: int) -> Event:
        event = select(Event).where(Event.event_id == event_id)
        result = await db.execute(event)
        return get_or_404(result.scalar_one_or_none(), detail="Event not found")

    async def delete_event(self, db: AsyncSession, event_id: int) -> None:
        event = await self.get_event_by_id(db, event_id)
        await db.delete(event)
        await db.commit()

    async def update_event(
        self, db: AsyncSession, event_id: int, event_update: EventUpdate
    ) -> Event:
        event = await self.get_event_by_id(db, event_id)

        updated_event = event_update.model_dump(exclude_unset=True)
        for key, value in updated_event.items():
            setattr(event, key, value)

        await db.commit()
        await db.refresh(event)
        return event
