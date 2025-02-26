import enum
import datetime
import pydantic
import re
from utils import airports as airpot_utils


_DATE_PATTERN = re.compile(r".*([0-9]{2})\/?([0-9]{2}).*")
_DATETIME_PATTERN = re.compile(r"([0-9]{2})\s?([0-9]{2}):?([0-9]{2})")
_FLIGHT_PATTERN = re.compile(r"([A-Z]{3})\/?([A-Z]{3})")


class ScheduleType(enum.Enum):
    STBY = "STBY"
    DAYOFF = "DAY OFF"


class DayLongSchedule(pydantic.BaseModel):
    type: str = pydantic.Field(...)
    date: datetime.date = pydantic.Field(...)

    def summary(self) -> str:
        return f"{self._emoji()}{self.type}"

    def description(self) -> str:
        return f"{self.type} on {self.date}"

    def _emoji(self) -> str:
        if self.type == ScheduleType.STBY.value:
            return "🤬"
        return "🌴"


class Flight(pydantic.BaseModel):
    departure_time: datetime.datetime = pydantic.Field(...)
    departure_airport: str = pydantic.Field(...)
    arrival_airport: str = pydantic.Field(...)
    arrival_time: datetime.datetime = pydantic.Field(...)

    def description(self) -> str:
        return f"{airpot_utils.get_airport_name_by_iata_code(self.departure_airport)} -> {airpot_utils.get_airport_name_by_iata_code(self.arrival_airport)}"

    def summary(self) -> str:
        return f"{self._emoji()}{self.departure_airport} -> {self.arrival_airport}"

    def _emoji(self) -> str:
        if self.arrival_airport == "ICN" or self.arrival_airport == "GMP":
            return "🛬"
        return "🛫"


def match_flight_pattern(raw_string: str) -> re.Match:
    return _FLIGHT_PATTERN.match(raw_string)


def match_datetime_pattern(raw_string: str) -> re.Match:
    return _DATETIME_PATTERN.match(raw_string)


def match_date_pattern(raw_string: str) -> re.Match:
    return _DATE_PATTERN.match(raw_string)
