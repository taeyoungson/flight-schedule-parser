from loguru import logger
import requests
from requests import exceptions

from . import config as openweather_config
from . import dto

_URL = "https://api.openweathermap.org/data/3.0/onecall"


def get_daily_weather(
    lat: float,
    lon: float,
    units: str = "metric",
    exclude: str = "current,minutely,hourly",
) -> list[dto.WeatherData]:
    config = openweather_config.load_config()

    try:
        response = requests.get(
            url=_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": config.api_key,
                "units": units,
                "exclude": exclude,
            },
        )
        response.raise_for_status()
        daily_response = response.json()["daily"]

        weathers = []
        for daily in daily_response:
            weathers.append(dto.WeatherData.from_response(daily))

        return weathers

    except exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")
        raise errh
