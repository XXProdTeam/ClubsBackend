from ics import Calendar, Event
from datetime import datetime

import tempfile


class CalendarService:
    def __init__(self):
        self.calendar = Calendar()
        self.event = Event()

    def create_event(
        self, name: str, start: datetime, end: datetime, description: str, location: str
    ):
        self.event.name = name
        self.event.start = start
        self.event.end = end
        self.event.description = description
        self.event.location = location
        self.calendar.events.add(self.event)

        temp = tempfile.NamedTemporaryFile(
            delete=False, suffix=".ics", mode="w", encoding="utf-8"
        )
        temp.writelines(self.calendar.serialize_iter())
        temp.close()

        return temp.name
