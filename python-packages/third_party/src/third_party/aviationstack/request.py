import enum

import requests

from . import airlines
from . import config as aviation_stack_config

_FLIGHTS = "https://api.aviationstack.com/v1/flights"
_TIMEOUT = 10


class FlightStatus(enum.Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    LANDED = "landed"
    CANCELLED = "cancelled"
    INCIDENT = "incident"
    DIVERTED = "diverted"


def get_live_flights(dep_iata: str, arr_iata: str, airline: str = "asiana") -> list[dict[str, str]]:
    config = aviation_stack_config.load_config()
    airline_info = airlines.get_airline_info(airline)

    try:
        response = requests.get(
            _FLIGHTS,
            params={
                "access_key": config.api_key,
                "dep_iata": dep_iata,
                "arr_iata": arr_iata,
                "airline_name": airline_info.airline_name,
                "airline_iata": airline_info.iata_code,
                "airline_icao": airline_info.icao_code,
            },
            timeout=_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()["data"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error getting flight data: {e}")
