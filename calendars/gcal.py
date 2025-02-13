import datetime

from gcsa import event
from gcsa import google_calendar as gcal
from google.oauth2 import credentials

from calendars import config as gcal_config


class GoogleCalendar:
    _config = gcal_config.load_config()

    def __init__(self):
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


if __name__ == "__main__":
    client = GoogleCalendar()
    client.create_event(
        summary="Test Event",
        timezone="Asia/Seoul",
        start=datetime.datetime.now(),
        end=datetime.datetime.now() + datetime.timedelta(hours=1),
    )
