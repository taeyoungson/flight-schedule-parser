import datetime
import re
import zoneinfo

from loguru import logger
from third_party.calendars import gcal
from third_party.kakao import client as kakaotalk
from third_party.kakao import watcher

from utils import airports as airport_utils
from utils import flights as flight_utils
from utils import times as time_utils


def _preprocess_raw_string(raw_string: str) -> list[str]:
    return re.sub(r"\n+", "\n", raw_string).split("\n")


def _includes_words_to_ignore(raw_string: str) -> bool:
    return raw_string in ["SHOWUP", "FLIGHT", "SECTOR"]


def _parse_flight_match_to_airports(match: re.Match) -> tuple[str, str]:
    departure_airport = match.group(1)
    arrival_airport = match.group(2)

    assert airport_utils.check_iata_code_exists(departure_airport), f"Invalid iata code: {departure_airport}"
    assert airport_utils.check_iata_code_exists(arrival_airport), f"Invalid iata code: {arrival_airport}"
    return departure_airport, arrival_airport


def _parse_date_match(match: re.Match) -> tuple[int, int, int]:
    day = int(match.group(1))
    hour = int(match.group(2))
    minute = int(match.group(3))
    return day, hour, minute


def _build_datetime(
    year: int, month: int, day_hour_minute: tuple[int, int, int], tzinfo: zoneinfo.ZoneInfo
) -> datetime.datetime:
    return datetime.datetime(year, month, *day_hour_minute, tzinfo=tzinfo)


def _get_total_flight_time(flights: list[flight_utils.Flight]) -> datetime.timedelta:
    diff = sum([f.arrival_time - f.departure_time for f in flights], datetime.timedelta())
    return datetime.timedelta(hours=diff.seconds // 3600, minutes=(diff.seconds // 60) % 60)


@watcher.report_error
def build_flight_schedule(raw_ocr_result: str, year: int | None = None, month: int | None = None) -> None:
    if not year and not month:
        year, month = datetime.datetime.now().year, datetime.datetime.now().month
    parsed = _preprocess_raw_string(raw_ocr_result)

    num_schedules = 0
    flights: list[flight_utils.Flight] = []
    for idx, chunk in enumerate(parsed):
        if _includes_words_to_ignore(chunk):
            continue

        flight_matches = flight_utils.match_flight_pattern(chunk)
        if flight_matches:
            departure_airport, arrival_airport = _parse_flight_match_to_airports(flight_matches)

            departure_date_match = flight_utils.match_datetime_pattern(parsed[idx + 1])
            arrival_date_match = flight_utils.match_datetime_pattern(parsed[idx + 2])

            assert departure_date_match, f"Invalid departure date: {parsed[idx + 1]}"
            assert arrival_date_match, f"Invalid arrival date: {parsed[idx + 2]}"

            departure_month = month
            arrival_month = month
            if departure_date_match.group(1) > arrival_date_match.group(1):
                if num_schedules == 0:
                    departure_month = month - 1
                else:
                    arrival_month = month + 1

            departure = _build_datetime(
                year,
                departure_month,
                _parse_date_match(departure_date_match),
                airport_utils.get_timezone_by_iata_code(departure_airport),
            )
            arrival = _build_datetime(
                year,
                arrival_month,
                _parse_date_match(arrival_date_match),
                airport_utils.get_timezone_by_iata_code(arrival_airport),
            )

            assert arrival > departure, f"Arrival time is earlier than departure time: {arrival} < {departure}"

            flights.append(
                flight_utils.Flight(
                    departure_time=departure,
                    departure_airport=departure_airport,
                    arrival_airport=arrival_airport,
                    arrival_time=arrival,
                )
            )
            num_schedules += 1

    logger.info(f"Number of schedules: {num_schedules}")
    calendar = gcal.load_google_calendar_client()

    # clear existing events in target events
    events_in_month = calendar.get_events(
        time_min=time_utils.get_start_of_the_month(year, month),
        time_max=time_utils.get_end_of_the_month(year, month),
    )
    calendar.delete_events(events_in_month)

    for f in flights:
        logger.info(f"Departure: {f.departure_time}, Arrival: {f.arrival_time}")
        calendar.create_event(
            summary=f.summary(),
            timezone="Asia/Seoul",
            start=f.departure_time,
            end=f.arrival_time,
            description=f.description(),
        )

    kakaotalk.send_to_me(
        f"""
        {year}-{month}
        Number of schedules: {num_schedules}
        Total flight time: {_get_total_flight_time(flights)}
        """
    )
