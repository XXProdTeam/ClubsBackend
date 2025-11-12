from ics import Calendar, Event
from datetime import datetime
import tempfile
import aiofiles
import logging
from zoneinfo import ZoneInfo

class CalendarService:
    def __init__(self):
        self.calendar = Calendar()
        self.moscow_tz = ZoneInfo("Europe/Moscow")

    async def create_event(
        self,
        name: str,
        start: datetime,
        end: datetime,
        description: str,
        location: str,
    ) -> str:
        event = Event()
        event.name = name
        event.begin = start.replace(tzinfo=self.moscow_tz)
        event.end = end.replace(tzinfo=self.moscow_tz)
        event.description = description
        event.location = location
        self.calendar.events.add(event)

        temp = tempfile.NamedTemporaryFile(
            delete=False, suffix=".ics", mode="w", encoding="utf-8"
        )

        try:
            async with aiofiles.open(temp.name, mode="w", encoding="utf-8") as f:
                async for line in self._serialize_async():
                    await f.write(line)
        except Exception as e:
            logging.error(f"Ошибка при создании .ics файла: {e}")
            raise
        finally:
            temp.close()

        return temp.name

    async def _serialize_async(self):
        """Асинхронный генератор для сериализации календаря."""
        for line in self.calendar.serialize_iter():
            yield line
