from loguru import logger
import requests
from requests import exceptions

from . import config as openweather_config
from . import dto

_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather_by_coord(
    lat: float, lon: float, units: str = "metric", mode: str = "json", cnt: int = 40
) -> list[dto.WeatherData]:
    config = openweather_config.load_config()

    try:
        response = requests.get(
            url=_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": config.api_key,
                "mode": mode,
                "units": units,
                "cnt": cnt,
            },
        )
        response.raise_for_status()

        weathers = []
        for w in response.json()["list"]:
            weathers.append(dto.WeatherData.from_response(w))
        return weathers

    except exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")
        raise errh
