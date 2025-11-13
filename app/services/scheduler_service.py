import logging
from datetime import timedelta, datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import Settings
from app.db.session import async_session_maker
from app.services.bot_notification_service import NotificationService

from zoneinfo import ZoneInfo

logging.basicConfig(level=logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.INFO)

settings = Settings()
notification_service = NotificationService()

jobstores = {"default": SQLAlchemyJobStore(url=settings.DATABASE_URL_SYNC)}

scheduler = AsyncIOScheduler(jobstores=jobstores)


async def send_one_day_before_event(user_id: int, event_id: int):
    async with async_session_maker() as db:
        await notification_service.one_day_before_event(
            db=db, user_id=user_id, event_id=event_id
        )


async def send_one_hour_before_event(user_id: int, event_id: int):
    async with async_session_maker() as db:
        await notification_service.one_hour_before_event(
            db=db, user_id=user_id, event_id=event_id
        )


async def send_feedback_link(user_id: int, event_id: int):
    async with async_session_maker() as db:
        await notification_service.event_feedback(
            db=db, user_id=user_id, event_id=event_id
        )


class ScheduleService:
    def __init__(self):
        self.scheduler = scheduler

    def schedule_reminder_one_day_before(
        self, event_id: int, user_id: int, remind_time: datetime
    ):
        """Создаёт задачу за 1 день до начала события."""
        remind_time = remind_time.replace(tzinfo=ZoneInfo("Europe/Moscow"))
        remind_time = remind_time - timedelta(seconds=10)
        # remind_time = remind_time - timedelta(days=1)

        self.scheduler.add_job(
            func=send_one_day_before_event,
            trigger="date",
            run_date=remind_time,
            args=[user_id, event_id],
            id=f"event_{event_id}_user_{user_id}_reminder_one_day_before",
            replace_existing=True,
        )

    def schedule_reminder_one_hour_before(
        self, event_id: int, user_id: int, remind_time: datetime
    ):
        """Создаёт задачу за 1 час до начала события."""
        remind_time = remind_time.replace(tzinfo=ZoneInfo("Europe/Moscow"))
        remind_time = remind_time - timedelta(seconds=5)
        # remind_time = remind_time - timedelta(hours=1)

        self.scheduler.add_job(
            func=send_one_hour_before_event,
            trigger="date",
            run_date=remind_time,
            args=[user_id, event_id],
            id=f"event_{event_id}_user_{user_id}_reminder_one_hour_before",
            replace_existing=True,
        )

    def schedule_reminder_feedback_link(
        self, event_id: int, user_id: int, remind_time: datetime
    ):
        """Создаёт задачу за 1 день до начала события."""
        remind_time = remind_time.replace(tzinfo=ZoneInfo("Europe/Moscow"))
        remind_time = remind_time + timedelta(seconds=1)
        # remind_time = remind_time + timedelta(hours=1)

        self.scheduler.add_job(
            func=send_feedback_link,
            trigger="date",
            run_date=remind_time,
            args=[user_id, event_id],
            id=f"event_{event_id}_user_{user_id}_reminder_feedback_link",
            replace_existing=True,
        )
