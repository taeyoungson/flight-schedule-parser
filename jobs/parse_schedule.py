from loguru import logger
import pytz

from calendars import gcal
from kakao import watcher
from utils import schedule

_OCR_DELIMITER = "\n"
_TIMEZONE = "Asia/Seoul"


@watcher.report
def build_flight_schedule(ocr_result: str) -> None:
    schedules = schedule.parse_schedule(ocr_result)

    calendar = gcal.GoogleCalendar()
    for s in schedules:
        logger.info(
            f"""
            Date: {s.date}
            Flight: {s.flight}
            STD: {s.std}
            STA: {s.sta}
            Depart At: {s.depart_at}
            Arrive At: {s.arrive_at}
        """
        )
        start = s.std
        end = None
        try:
            start = s.std.astimezone(pytz.timezone(_TIMEZONE))
            end = s.sta.astimezone(pytz.timezone(_TIMEZONE))
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(e)
        finally:
            calendar.create_event(
                summary=s.summary(),
                timezone="Asia/Seoul",
                start=start,
                end=end,
                description=s.description(),
            )
