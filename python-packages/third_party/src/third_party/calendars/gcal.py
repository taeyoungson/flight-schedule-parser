import datetime
from typing import Iterable

from gcsa import event
from gcsa import google_calendar as gcal
from google.oauth2 import credentials

from . import config as gcal_config


class GoogleCalendar:
    def __init__(self):
        self._config = gcal_config.load_config()
        self._credentials = credentials.Credentials(
            token=self._config.token,
            token_uri=self._config.token_uri,
            client_id=self._config.client_id,
            client_secret=self._config.client_secret,
            refresh_token=self._config.refresh_token,
        )
        self._calendar = gcal.GoogleCalendar(
            default_calendar=self._config.calendar_id,
            credentials=self._credentials,
            open_browser=False,
        )

    def _create_event(self, evt: event.Event) -> None:
        self._calendar.add_event(evt)

    def _get_events(
        self, time_min: datetime.datetime, time_max: datetime.datetime, timezone: str = "Asia/Seoul"
    ) -> Iterable[event.Event]:
        return self._calendar.get_events(time_min=time_min, time_max=time_max, timezone=timezone)

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

    def get_events(
        self, time_min: datetime.datetime, time_max: datetime.datetime, timezone: str = "Asia/Seoul"
    ) -> list[event.Event]:
        return list(self._get_events(time_min, time_max, timezone))

    def _delete_event(self, evt: event.Event) -> None:
        self._calendar.delete_event(evt)

    def delete_events(self, evts: list[event.Event]) -> None:
        for e in evts:
            self._delete_event(e)


def load_google_calendar_client():
    return GoogleCalendar()
