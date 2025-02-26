import enum
import datetime
import zoneinfo


class TimeZone(enum.Enum):
    SEOUL = zoneinfo.ZoneInfo("Asia/Seoul")
    UTC = zoneinfo.ZoneInfo("UTC")


def now() -> datetime.datetime:
    return datetime.datetime.now(TimeZone.SEOUL.value)


def hours_before(datetime_: datetime.datetime, hours: int) -> datetime.datetime:
    return datetime_ - datetime.timedelta(hours=hours)


def minutes_before(datetime_: datetime.datetime, minutes: int) -> datetime.datetime:
    return datetime_ - datetime.timedelta(minutes=minutes)


def minutes_after(datetime_: datetime.datetime, minutes: int) -> datetime.datetime:
    return datetime_ + datetime.timedelta(minutes=minutes)


def get_today_as_date() -> datetime.date:
    return now().date()


def get_next_month(year: int, month: int) -> tuple[int, int]:
    if month == 12:
        return year + 1, 1
    return year, month + 1


def get_days_in_month(year: int, month: int) -> int:
    if month == 12:
        return (datetime.datetime(year + 1, 1, 1) - datetime.datetime(year, month, 1)).days
    return (datetime.datetime(year, month + 1, 1) - datetime.datetime(year, month, 1)).days


def get_start_of_the_day(date: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(date, datetime.time.min)


def get_end_of_the_day(date: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(date, datetime.time.max)


def parse_datetime(datetime_string: str) -> datetime.datetime:
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S+00:00")


def format_datetime(datetime_: datetime.datetime) -> str:
    return datetime_.strftime("%Y-%m-%dT%H:%M:%S%z")


def pretty_datetime(datetime_: datetime.datetime) -> str:
    hours = datetime_.hour
    minutes = datetime_.minute

    prefix = "오전" if hours < 12 else "오후"
    if hours > 12:
        hours -= 12

    return f"{prefix} {hours:02d}시 {minutes:02d}분"


def to_timezone(datetime_: datetime.datetime, tzinfo: zoneinfo.ZoneInfo) -> datetime.datetime:
    return datetime_.astimezone(tzinfo=tzinfo)
