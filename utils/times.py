import datetime
import enum
import zoneinfo


class TimeZone(enum.Enum):
    SEOUL = zoneinfo.ZoneInfo("Asia/Seoul")
    UTC = zoneinfo.ZoneInfo("UTC")


class DateTimeFormatter(enum.Enum):
    DATE = "%Y-%m-%d"
    FULL = "%Y-%m-%dT%H:%M:%S+00:00"
    COMPACTDATE = "%m/%d"
    COMPACTDATE_KR = "%m월 %d일"

    def format(self, datetime_: datetime.datetime) -> str:
        return datetime_.strftime(self.value)

    def parse(self, datetime_string: str) -> datetime.datetime:
        return datetime.datetime.strptime(datetime_string, self.value)


def now() -> datetime.datetime:
    return datetime.datetime.now(TimeZone.SEOUL.value)


def get_days_before(date: datetime.date, days: int) -> datetime.date:
    return date - datetime.timedelta(days=days)


def get_days_after(date: datetime.date, days: int) -> datetime.date:
    return date + datetime.timedelta(days=days)


def hours_before(datetime_: datetime.datetime, hours: int) -> datetime.datetime:
    return datetime_ - datetime.timedelta(hours=hours)


def hours_after(datetime_: datetime.datetime, hours: int) -> datetime.datetime:
    return datetime_ + datetime.timedelta(hours=hours)


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


def get_start_of_the_month(year: int, month: int) -> datetime.datetime:
    return datetime.datetime(year, month, 1, 0, 0, 0)


def get_end_of_the_month(year: int, month: int) -> datetime.datetime:
    if month == 12:
        return datetime.datetime(year + 1, 1, 1, 23, 59, 59) - datetime.timedelta(days=1)
    return datetime.datetime(year, month + 1, 1, 23, 59, 59) - datetime.timedelta(days=1)


def parse_datetime(datetime_string: str) -> datetime.datetime:
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S+00:00")


def format_datetime(datetime_: datetime.datetime) -> str:
    return datetime_.strftime("%Y-%m-%dT%H:%M:%S%z")


def pretty_datetime(datetime_: datetime.datetime) -> str:
    month = datetime_.month
    day = datetime_.day
    hours = datetime_.hour
    minutes = datetime_.minute

    prefix = "오전" if hours < 12 else "오후"
    if hours > 12:
        hours -= 12

    return f"{month: 02}월 {day: 02}일 {prefix} {hours:02d}시 {minutes:02d}분"


def to_timezone(datetime_: datetime.datetime, tzinfo: zoneinfo.ZoneInfo) -> datetime.datetime:
    return datetime_.astimezone(tz=tzinfo)


def is_datetime_between(datetime_: datetime.datetime, start: datetime.datetime, end: datetime.datetime) -> bool:
    return start <= datetime_ <= end


def is_date_between(date: datetime.date, start: datetime.date, end: datetime.date) -> bool:
    return start <= date <= end
