import dataclasses
import zoneinfo

import airportsdata as apt

_AIRPORTS = apt.load("IATA")


@dataclasses.dataclass
class Coord:
    lat: float
    lon: float


def get_coord_by_iata_code(iata: str) -> Coord:
    airport_data = _AIRPORTS[iata]
    return Coord(
        lat=float(airport_data["lat"]),
        lon=float(airport_data["lon"]),
    )


def get_timezone_by_iata_code(iata: str) -> zoneinfo.ZoneInfo:
    return zoneinfo.ZoneInfo(_AIRPORTS[iata].get("tz"))


def get_airport_name_by_iata_code(iata: str) -> str:
    return _AIRPORTS[iata].get("name")


def check_iata_code_exists(iata_code: str) -> bool:
    return iata_code in _AIRPORTS


def get_cityname_by_iata_code(iata_code: str) -> str:
    return _AIRPORTS[iata_code].get("city")
