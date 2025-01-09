import datetime

from gcsa import event
from gcsa import google_calendar as gcal

from calendars import config as gcal_config


class GoogleCalendar:
    _config = gcal_config.load_config()

    def __init__(self):
        self._calendar = gcal.GoogleCalendar(
            default_calendar=self._config.calendar_id,
        )

    def _create_event(self, evt: event.Event) -> None:
        self._calendar.add_event(evt)

    def create_event(
        self,
        summary: str,
        timezone: str,
        start: datetime.datetime | datetime.date,
        end: datetime.datetime | None = None,
        recurrence: str | None = None,
        description: str | None = None,
        location: str | None = None,
    ) -> None:
        evt = event.Event(
            summary=summary,
            timezone=timezone,
            start=start,
            end=end,
            recurrence=recurrence,
            description=description,
            location=location,
        )
        self._create_event(evt)
