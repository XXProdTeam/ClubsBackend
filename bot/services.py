from maxapi import Bot

import logging

from maxapi.methods.types.sended_message import SendedMessage

from bot.keyboards import hide_text_payload

from app.db.session import get_async_session
from app.core.config import Settings
from app.crud.user import UserCRUD

settings = Settings()
user_crud = UserCRUD()


async def get_db_session():
    async for session in get_async_session():
        try:
            yield session
        finally:
            await session.close()


async def send_notification(chat_id: int, text: str) -> None:
    """
    Асинхронно отправляет уведомление пользователю от имени бота.
    """
    logging.info(f"Отправка уведомления пользователю в чат {chat_id}: '{text}'")
    try:
        bot = Bot(token=settings.BOT_TOKEN)
        sended_message: SendedMessage = await bot.send_message(
            chat_id=chat_id, text=text, attachments=[hide_text_payload]
        )
        print(sended_message.message.body.mid)
        await bot.session.close()
        logging.info(f"Уведомление в чат {chat_id} успешно отправлено.")
    except Exception as e:
        logging.error(
            f"Ошибка при отправке уведомления пользователю в чат {chat_id}: {e}"
        )
