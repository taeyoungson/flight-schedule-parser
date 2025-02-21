import pydantic


class AirlineInfo(pydantic.BaseModel):
    id: str
    fleet_average_age: str
    airline_id: str
    callsign: str
    hub_code: str
    iata_code: str
    icao_code: str
    country_iso2: str
    date_founded: str
    iata_prefix_accounting: str
    airline_name: str
    country_name: str
    fleet_size: str
    status: str
    type: str


AIRLINES = [
    (
        "asiana",
        AirlineInfo(
            id="3638267",
            fleet_average_age="10.3",
            airline_id="67",
            callsign="ASIANA",
            hub_code="ICN",
            iata_code="oz",
            icao_code="aar",
            country_iso2="KR",
            date_founded="1988",
            iata_prefix_accounting="988",
            airline_name="asiana airlines",
            country_name="South Korea",
            fleet_size="84",
            status="active",
            type="scheduled",
        ),
    ),
]


AIRLINES_DICT = {name: info for name, info in AIRLINES}


def get_airline_info(name: str) -> AirlineInfo:
    assert name in AIRLINES_DICT, f"Airline {name} not found"
    return AIRLINES_DICT[name]
