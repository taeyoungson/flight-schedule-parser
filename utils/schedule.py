import dataclasses
import datetime
import enum
import re

from loguru import logger
import pytz

from utils import airports as apt
from utils import times

_DATE_PATTERN = re.compile(r"[0-9]{2}\/[0-9]{2}")
_FLIGHT_PATTERN = re.compile(r"[A-Z]{3}\/[A-Z]{3}")
_TIME_PATTERN = re.compile(r"[A-Z,0-9]{2}[ :.]*[A-Z,0-9]{2}:[0-9]{2}")

_REPLACE_DICT = {
    "O": "0",
    "I": "1",
    "S": "5",
    "B": "8",
    "Z": "2",
    "G": "6",
    "A": "4",
    "L": "1",
    "T": "7",
    "J": "1",
    "Q": "0",
    "D": "0",
    "R": "0",
    "C": "0",
    "F": "0",
    "H": "0",
    "K": "0",
    "M": "0",
    "N": "0",
    "P": "0",
    "U": "0",
    "V": "0",
    "W": "0",
    "X": "0",
    "Y": "0",
}


class ScheduleType(enum.Enum):
    DAY_OFF = "DAY OFF"
    STBY = "STBY"


@dataclasses.dataclass
class Schedule:
    date: datetime.datetime
    flight: str
    showup: datetime.datetime | None = None
    sector: str | None = None
    std: datetime.datetime | datetime.date | None = None
    sta: datetime.datetime | datetime.date | None = None
    depart_at: str | None = None
    arrive_at: str | None = None

    def summary(self) -> str:
        match self.flight:
            case ScheduleType.DAY_OFF.value:
                return "🌴OFF"
            case ScheduleType.STBY.value:
                return "🤬STBY"
            case _:
                pass

        if self.arrive_at == "Incheon International Airport":
            emoji = "🛬"
        elif self.depart_at == "Incheon International Airport":
            emoji = "🛫"
        else:
            emoji = "✈️"

        return f"{emoji}{self.flight.replace('/', ' - ')}"

    def description(self) -> str:
        match self.flight:
            case ScheduleType.DAY_OFF.value:
                return "쉬 는 날"
            case ScheduleType.STBY.value:
                return "오프나왔으면..."
            case _:
                pass
        return f"출발: {self.depart_at}\n도착: {self.arrive_at}"


def _parse_single_flight_schedule(year: int, month: int, day: int, flight: str, timestring: str) -> Schedule | None:
    for k, v in _REPLACE_DICT.items():
        timestring = timestring.replace(k, v)

    time_repr = _TIME_PATTERN.findall(timestring)
    assert len(time_repr) == 2, logger.error(
        f"Invalid number of matches, {year}-{month}-{day}, {len(time_repr)}, matches: {time_repr}"
    )

    airports = flight.split("/")

    if not apt.check_iata_code_exists(airports[0]) or not apt.check_iata_code_exists(airports[1]):
        return None

    depart_tz = pytz.timezone(apt.get_timezone_by_iata_code(airports[0]))
    arrive_tz = pytz.timezone(apt.get_timezone_by_iata_code(airports[1]))
    depart_at = apt.get_airport_name_by_iata_code(airports[0])
    arrive_at = apt.get_airport_name_by_iata_code(airports[1])

    std, sta = time_repr
    std = depart_tz.localize(datetime.datetime(year, month, int(std[0:2]), int(std[-5:-3]), int(std[-2:])))
    sta = arrive_tz.localize(datetime.datetime(year, month, int(sta[0:2]), int(sta[-5:-3]), int(sta[-2:])))

    if sta < std:
        sta = sta.replace(month=month + 1)

    assert sta > std, logger.error(f"Arrival time is earlier than departure time, airports: {airports} {sta} < {std}")

    return Schedule(
        date=datetime.datetime(year, month, day),
        flight=flight,
        std=std,
        sta=sta,
        depart_at=depart_at,
        arrive_at=arrive_at,
    )


def parse_schedule(year: int, month: int, rows: list[str]) -> list[Schedule]:
    start = 0
    while True:
        if _DATE_PATTERN.search(rows[start]):
            break
        start += 1

    rows = rows[start:]
    cur_month_days = times.get_days_in_month(year, month)
    schedules = []
    for day in range(cur_month_days):
        if day >= len(rows):
            break
        if ScheduleType.DAY_OFF.value in rows[day]:
            schedules.append(
                Schedule(
                    date=datetime.datetime(year, month, day + 1),
                    flight=ScheduleType.DAY_OFF.value,
                    std=datetime.date(year, month, day + 1),
                )
            )
        elif ScheduleType.STBY.value in rows[day]:
            schedules.append(
                Schedule(
                    date=datetime.datetime(year, month, day + 1),
                    flight=ScheduleType.STBY.value,
                    std=datetime.date(year, month, day + 1),
                )
            )

        is_flight_exists = _FLIGHT_PATTERN.search(rows[day])
        if is_flight_exists:
            flight = _FLIGHT_PATTERN.findall(rows[day])

            if len(flight) == 1:
                timestring = rows[day][is_flight_exists.end() :]
                schedule = _parse_single_flight_schedule(year, month, day + 1, flight[0], timestring)
                if schedule:
                    schedules.append(schedule)

            elif len(flight) > 1:
                inner_rows = rows[day].split("\n")
                for row in inner_rows:
                    is_flight_exists = _FLIGHT_PATTERN.search(row)
                    if is_flight_exists:
                        timestring = row[is_flight_exists.end() :]
                        schedule = _parse_single_flight_schedule(
                            year, month, day + 1, is_flight_exists.group(), timestring
                        )
                        if schedule:
                            schedules.append(schedule)
        else:
            continue

    return schedules


def parse_schedule_month(rows: list[str]) -> str:
    months_candidate = []
    for row in rows:
        date = _DATE_PATTERN.search(row)
        if date:
            months_candidate.append(date.group()[:2])
    return max(set(months_candidate), key=months_candidate.count)
