import datetime

from loguru import logger
from PIL import Image
import pytz

from calendars import gcal
from utils import ocr
from utils import schedule

_OCR_DELIMITER = "\n\n"
_TIMEZONE = "Asia/Seoul"


def get_flight_schedule(img: Image.Image) -> None:
    extracted = ocr.image_to_string(img).split(_OCR_DELIMITER)
    month = int(schedule.parse_schedule_month(extracted))

    if datetime.datetime.now().month > month:
        year = datetime.datetime.now().year + 1
    else:
        year = datetime.datetime.now().year
    logger.info(f"Parsing schedule for {year} - {month}")
    schedules = schedule.parse_schedule(year, month, extracted)

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
