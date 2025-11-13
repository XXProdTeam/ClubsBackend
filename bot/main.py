import asyncio
import logging

from maxapi import Bot, Dispatcher
from maxapi.filters.command import Command
from maxapi.types import (
    OpenAppButton,
    MessageCreated,
    ButtonsPayload,
    BotStarted,
    MessageCallback,
    BotCommand,
)

from app.db.session import get_async_session
from app.crud.user import UserCRUD
from app.core.config import Settings
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)

settings = Settings()
user_crud = UserCRUD()

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher()


async def startup(event: BotStarted | MessageCreated):
    buttons = [
        [
            OpenAppButton(
                text="Открыть приложение",
                web_app=event.bot.me.username,
                contact_id=event.bot.me.user_id,
            )
        ]
    ]
    buttons_payload = ButtonsPayload(buttons=buttons).pack()
    await event.bot.send_message(
        chat_id=event.chat.chat_id,
        text="Привет! Это бот для организации мероприятий и клубов университета.\n\nДля начала работы нажмите кнопку ниже.",
        attachments=[buttons_payload],
    )


async def create_user(new_user: UserCreate):
    async for db in get_async_session():
        if not await user_crud.get_user_by_id_raw(db, new_user.user_id):
            await user_crud.create_user(db=db, user=new_user)
        break


@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.set_my_commands(
        BotCommand(name="start", description="Регистрация пользователя")
    )
    logging.info(
        f"Пользователь {event.message.sender.user_id} - {event.message.sender.first_name} {event.message.sender.last_name} запустил бота"
    )
    new_user = UserCreate(
        user_id=event.user.user_id,
        first_name=event.user.first_name,
        last_name=event.user.last_name if event.user.last_name else "",
        chat_id=event.chat_id,
    )

    await create_user(new_user=new_user)

    await startup(event=event)


@dp.message_created(Command("start"))
async def start(event: MessageCreated):
    logging.info(
        f"Пользователь {event.message.sender.user_id} - {event.message.sender.first_name} {event.message.sender.last_name} запустил команду /start"
    )
    new_user = UserCreate(
        user_id=event.message.sender.user_id,
        first_name=event.message.sender.first_name,
        last_name=event.message.sender.last_name,
        chat_id=event.chat.chat_id,
    )

    await create_user(new_user=new_user)

    await startup(event=event)


@dp.message_callback()
async def message_callback(callback: MessageCallback):
    logging.info(
        f"Пользователь {callback.message.sender.user_id} - {callback.message.sender.first_name} {callback.message.sender.last_name} нажал кнопку `скрыть сообщение`"
    )
    await callback.bot.delete_message(message_id=callback.message.body.mid)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
