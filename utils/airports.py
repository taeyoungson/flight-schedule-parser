import zoneinfo

import airportsdata as apt

_AIRPORTS = apt.load("IATA")


def get_timezone_by_iata_code(iata: str) -> zoneinfo.ZoneInfo:
    return zoneinfo.ZoneInfo(_AIRPORTS[iata].get("tz"))


def get_airport_name_by_iata_code(iata: str) -> str:
    return _AIRPORTS[iata].get("name")


def check_iata_code_exists(iata_code: str) -> bool:
    return iata_code in _AIRPORTS
