from loguru import logger
from third_party.aviationstack import request as aviation_request
from third_party.kakao import client as kakaotalk
from utils import times as time_utils


_MIN_DELAY = 20


def _filter_flights_of_interest(flights: list[dict[str, str]]) -> list[dict]:
    return list(
        filter(
            lambda flight: flight["flight_status"] == aviation_request.FlightStatus.ACTIVE.value
            and flight["flight_date"] == time_utils.get_today_as_date().strftime("%Y-%m-%d"),
            flights,
        )
    )


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
    total_delay = departure_delay + arrival_delay
    scheduled_arrival = time_utils.parse_datetime(flight["arrival"]["scheduled"])

    if departure_delay + arrival_delay >= _MIN_DELAY:
        kakaotalk.send_to_me(
            f"""
                비행 {flight["flight"]["iata"]}편이 지연되었어요 😓
                출발지: {flight["departure"]["airport"]}
                도착지: {flight["arrival"]["airport"]}
                지연됨: 총 {total_delay}분 (출발: {departure_delay}분, 도착: {arrival_delay}분)
                도착예정시간: {time_utils.pretty_datetime(time_utils.minutes_after(scheduled_arrival, total_delay))}
            """
        )
