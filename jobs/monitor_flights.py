import datetime
import zoneinfo

from loguru import logger
from third_party.aviationstack import request as aviation_request
from third_party.discord import client as discord
from third_party.discord import settings as discord_settings
from third_party.kakao import watcher

from utils import airports as airport_utils
from utils import times as time_utils


def _filter_flights_of_interest(
    flights: list[dict[str, str]], flight_start: datetime.datetime, flight_end: datetime.datetime
) -> dict:
    for f in flights:
        dep_tz = airport_utils.get_timezone_by_iata_code(f["departure"]["iata"])
        arr_tz = airport_utils.get_timezone_by_iata_code(f["arrival"]["iata"])
        dep = time_utils.DateTimeFormatter.FULL.parse(f["departure"]["scheduled"]).replace(tzinfo=dep_tz)
        arr = time_utils.DateTimeFormatter.FULL.parse(f["arrival"]["scheduled"]).replace(tzinfo=arr_tz)

        if dep == flight_start and arr == flight_end:
            return f
    raise ValueError("No flight found", flights)


def _parse_and_convert_to_kst(datetime_str: str, tz: str) -> datetime.datetime:
    dt = time_utils.parse_datetime(datetime_str).replace(tzinfo=zoneinfo.ZoneInfo(tz))
    return dt.astimezone(time_utils.TimeZone.SEOUL.value)


@watcher.report_error
def main(
    flight_start: datetime.datetime,
    flight_end: datetime.datetime,
    dep_iata: str,
    arr_iata: str,
    airline: str = "asiana",
) -> None:
    logger.debug(f"Monitor Flights: {dep_iata} -> {arr_iata} ({airline})")
    flights = aviation_request.get_live_flights(
        dep_iata=dep_iata,
        arr_iata=arr_iata,
        airline=airline,
    )

    flight_found = _filter_flights_of_interest(flights, flight_start, flight_end)
    logger.debug(f"Flight Found: {flight_found}")

    departure_delay = flight_found["departure"]["delay"] or 0
    arrival_delay = flight_found["arrival"]["delay"] or 0
    scheduled_departure = _parse_and_convert_to_kst(
        flight_found["departure"]["scheduled"], flight_found["departure"]["timezone"]
    )
    scheduled_arrival = _parse_and_convert_to_kst(
        flight_found["arrival"]["scheduled"], flight_found["arrival"]["timezone"]
    )

    scheduled_departure = time_utils.minutes_after(scheduled_departure, departure_delay)
    scheduled_arrival = time_utils.minutes_after(scheduled_arrival, arrival_delay)

    discord.send_to_dev(
        f"<@{discord_settings.ME}>님!\n"
        + f"향공편 {flight_found['flight']['iata']}편을 조회했어요.\n"
        + f"**조회 날짜: {time_utils.get_today_as_date()}**\n"
        + "```\n"
        + f"현재 상태: {flight_found['flight_status'].upper()}\n"
        + f"🛫 출발지: {flight_found['departure']['airport']}\n"
        + f"🛬 도착지: {flight_found['arrival']['airport']}\n"
        + f"출발 지연: 총 {departure_delay}분\n"
        + f"도착 지연: 총 {arrival_delay}분\n"
        + f"출발 시각 (KST): {time_utils.pretty_datetime(scheduled_departure)}\n"
        + f"도착 예정 (KST): {time_utils.pretty_datetime(scheduled_arrival)}\n"
        "```"
    )
