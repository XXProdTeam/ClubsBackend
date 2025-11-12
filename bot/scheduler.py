import asyncio
import logging

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import Settings

logging.basicConfig(level=logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.INFO)

settings = Settings()


jobstores = {"default": SQLAlchemyJobStore(url=settings.DATABASE_URL_SYNC)}

scheduler = AsyncIOScheduler(jobstores=jobstores)


async def main():
    logging.info("Запуск планировщика...")
    scheduler.start()
    while True:
        await asyncio.sleep(1000)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Остановка планировщика.")
        scheduler.shutdown()
