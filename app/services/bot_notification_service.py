from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.bot_services import send_notification
from bot.keyboards import hide_text_payload

from app.crud.user import UserCRUD
from app.crud.event import EventCRUD

from maxapi.types import LinkButton, ButtonsPayload, CallbackButton


class NotificationService:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.event_crud = EventCRUD()

    async def register_event(
        self, db: AsyncSession, user_id: int, event_id: int
    ) -> None:
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        await send_notification(
            chat_id=user.chat_id,
            text=f"Вы зарегистрированы на мероприятие\nСобытие: {event.name}",
            attachments=[hide_text_payload],
        )

    async def unregister_event(
        self, db: AsyncSession, user_id: int, event_id: int
    ) -> None:
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        await send_notification(
            chat_id=user.chat_id,
            text=f"Вы отменили регистрацию на мероприятие\nСобытие: {event.name}",
            attachments=[hide_text_payload],
        )

    async def one_day_before_event(
        self, db: AsyncSession, user_id: int, event_id: int
    ) -> None:
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        await send_notification(
            chat_id=user.chat_id,
            text=f"Напоминание о мероприятии!\n"
            f"Завтра состоится событие: {event.name}\n\n"
            f"Где: {event.place}\n"
            f"Когда: {event.start_time.strftime('%d.%m.%Y %H:%M')}",
            attachments=[hide_text_payload],
        )

    async def one_hour_before_event(
        self, db: AsyncSession, user_id: int, event_id: int
    ) -> None:
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        await send_notification(
            chat_id=user.chat_id,
            text=f"Напоминание о мероприятии!\n"
            f"Через час состоится событие: {event.name}\n\n"
            f"Где: {event.place}\n"
            f"Когда: {event.start_time.strftime('%d.%m.%Y %H:%M')}",
            attachments=[hide_text_payload],
        )

    async def event_feedback(self, db: AsyncSession, user_id: int, event_id: int):
        user = await self.user_crud.get_user_by_id(db=db, user_id=user_id)
        event = await self.event_crud.get_event_by_id(db=db, event_id=event_id)

        link_buttons = [
            [LinkButton(text="Ответить", url=event.feedback_link)],
            [
                CallbackButton(text="Скрыть", payload="hide"),
            ],
        ]

        button_payload = ButtonsPayload(buttons=link_buttons).pack()

        await send_notification(
            chat_id=user.chat_id,
            text=event.feedback_text,
            attachments=[button_payload],
        )
