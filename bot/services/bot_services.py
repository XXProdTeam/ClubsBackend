from maxapi import Bot

import logging

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


async def send_notification(chat_id: int, text: str, attachments: list) -> None:
    """
    Асинхронно отправляет уведомление пользователю от имени бота.
    """
    try:
        bot = Bot(token=settings.BOT_TOKEN)
        await bot.send_message(chat_id=chat_id, text=text, attachments=attachments)
        await bot.session.close()
    except Exception as e:
        logging.error(
            f"Ошибка при отправке уведомления пользователю в чат {chat_id}: {e}"
        )


async def send_file(chat_id: int, text: str, attachment: list) -> None:
    attachments = attachment + [hide_text_payload]
    try:
        bot = Bot(token=settings.BOT_TOKEN)
        await bot.send_message(chat_id=chat_id, text=text, attachments=attachments)
        await bot.session.close()
    except Exception as e:
        logging.error(f"Ошибка при отправке файла пользователю в чат {chat_id}: {e}")
