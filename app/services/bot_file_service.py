from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.bot_services import send_file

from app.crud.user import UserCRUD
from app.crud.event import EventCRUD

from app.services.calendar_service import CalendarService

from maxapi.types import InputMedia, LinkButton, ButtonsPayload


class FileService:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.event_crud = EventCRUD()
        self.calendar_service = CalendarService()

    async def send_ics(self, db: AsyncSession, user_id: int, event_id: int):
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        calendar_path = await self.calendar_service.create_event(
            name=event.name,
            start=event.start_time,
            end=event.end_time,
            description=event.description,
            location=event.place,
        )

        dt = datetime.fromisoformat(str(event.start_time))
        formatted_dt = dt.strftime("%d.%m.%Y %H:%M")

        await send_file(
            chat_id=user.chat_id,
            text=f"Событие: {event.name}\nГде: {event.place}\n"
            f"Когда: {formatted_dt}\n\nИмпортируйте его в ваш календарь",
            attachment=[InputMedia(path=calendar_path)],
        )
