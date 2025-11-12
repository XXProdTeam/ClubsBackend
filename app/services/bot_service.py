from sqlalchemy.ext.asyncio import AsyncSession

from bot.services import send_notification, send_file

from app.crud.user import UserCRUD
from app.crud.event import EventCRUD

from app.services.calendar_service import CalendarService

class NotificationService:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.event_crud = EventCRUD()

    async def register_event(self, db: AsyncSession, user_id: int, event_id: int) -> None:
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        await send_notification(
            chat_id=user.chat_id, text=f"Вы зарегистрированы на событие: {event.name}"
        )

    async def unregister_event(self, db: AsyncSession, user_id: int, event_id: int) -> None:
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        await send_notification(
            chat_id=user.chat_id,
            text=f"Вы отменили регистрацию на событие: {event.name}",
        )

    async def one_day_before_event(self, db: AsyncSession, user_id: int, event_id: int) -> None:
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        await send_notification(
            chat_id=user.chat_id, text=f"До события: {event.name} остался 1 день"
        )

    async def one_hour_before_event(
        self, db: AsyncSession, user_id: int, event_id: int
    ) -> None:
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        await send_notification(
            chat_id=user.chat_id, text=f"До события: {event.name} остался 1 час"
        )

class FileService:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.event_crud = EventCRUD()
        self.calendar_service = CalendarService()

    async def send_ics(self, db: AsyncSession, user_id: int, event_id: int):
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        calendar_path = self.calendar_service.create_event(
            name=event.name,
            start=event.start_time,
            end=event.end_time,
            description=event.description,
            location=event.place,
        )

        await send_file(
            chat_id=user.chat_id,
            text=f"Событие: {event.name}",
            attachment=[calendar_path]
        )