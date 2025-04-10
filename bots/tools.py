import datetime

from langchain import tools
from third_party.calendars import gcal


@tools.tool
def get_calendar_event(time_min: datetime.datetime, time_max: datetime.datetime) -> str:
    """
    Get events from google calendar starting from time_min to time_max in Asia/Seoul time zone.
    My girlfriend(현아, Hyun-A) is stewardess, and this calendar is composed of her flight schedule.
    """
    client = gcal.load_google_calendar_client()
    events = client.get_events(time_min, time_max)

    repr = ""
    for e in events:
        repr += f"""
            Event: {e.summary}
            Starts: {e.start}
            Ends: {e.end}
            Description: {e.description}
            \n
        """
    return repr
