import datetime
import zoneinfo

from loguru import logger
from third_party.aviationstack import request as aviation_request
from third_party.discord import client as discord
from third_party.discord import settings as discord_settings
from third_party.kakao import watcher

from utils import times as time_utils


def _filter_flights_of_interest(flights: list[dict[str, str]]) -> list[dict]:
    return list(
        filter(
            lambda flight: flight["flight_status"] == aviation_request.FlightStatus.ACTIVE.value
            and flight["flight_date"] == time_utils.get_today_as_date().strftime("%Y-%m-%d"),
            flights,
        )
    )


def _parse_and_convert_to_kst(datetime_str: str, tz: str) -> datetime.datetime:
    dt = time_utils.parse_datetime(datetime_str).replace(tzinfo=zoneinfo.ZoneInfo(tz))
    return dt.astimezone(time_utils.TimeZone.SEOUL.value)


@watcher.report_error
def main(dep_iata: str, arr_iata: str, airline: str = "asiana") -> None:
    logger.debug(f"Monitor Flights: {dep_iata} -> {arr_iata} ({airline})")
    flights = aviation_request.get_live_flights(
        dep_iata=dep_iata,
        arr_iata=arr_iata,
        airline=airline,
    )

    flights_of_interests = _filter_flights_of_interest(flights)
    assert len(flights_of_interests) == 1, (
        f"Expected 1 flight, but got {len(flights_of_interests)}, {flights_of_interests}"
    )

    flight = flights_of_interests[0]
    logger.debug(f"Flight Found: {flight}")

    departure_delay = flight["departure"]["delay"] or 0
    arrival_delay = flight["arrival"]["delay"] or 0
    actual_departure = _parse_and_convert_to_kst(flight["departure"]["actual"], flight["departure"]["timezone"])
    scheduled_arrival = _parse_and_convert_to_kst(flight["arrival"]["scheduled"], flight["arrival"]["timezone"])
    scheduled_arrival = time_utils.minutes_after(scheduled_arrival, arrival_delay)

    discord.send_to_flight(
        f"<@{discord_settings.ME}>님!\n" + f"향공편 {flight['flight']['iata']}편을 조회했어요.\n" + "```\n"
        f"출발지: {flight['departure']['airport']}\n"
        + f"도착지: {flight['arrival']['airport']}\n"
        + f"출발 지연: 총 {departure_delay}분\n"
        + f"도착 지연: 총 {arrival_delay}분\n"
        + f"실제 출발: {time_utils.pretty_datetime(actual_departure)}\n"
        + f"도착 예정: {time_utils.pretty_datetime(scheduled_arrival)}\n"
        "```"
    )
