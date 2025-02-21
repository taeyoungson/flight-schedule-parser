import datetime


def hours_before(datetime_: datetime.datetime, hours: int) -> datetime.datetime:
    return datetime_ - datetime.timedelta(hours=hours)


def get_today_as_date() -> datetime.date:
    return datetime.date.today()


def get_next_month(year: int, month: int) -> tuple[int, int]:
    if month == 12:
        return year + 1, 1
    return year, month + 1


def get_days_in_month(year: int, month: int) -> int:
    if month == 12:
        return (datetime.datetime(year + 1, 1, 1) - datetime.datetime(year, month, 1)).days
    return (datetime.datetime(year, month + 1, 1) - datetime.datetime(year, month, 1)).days
