from __future__ import annotations

import dataclasses
import datetime
import zoneinfo


@dataclasses.dataclass
class Temperature:
    avg: float
    max: float
    min: float
    feels_like: float


@dataclasses.dataclass
class Weather:
    id: str
    main: str
    description: str
    icon: str

    @classmethod
    def from_dict(cls, data: dict) -> Weather:
        return cls(
            id=data["id"],
            main=data["main"],
            description=data["description"],
            icon=data["icon"],
        )


@dataclasses.dataclass
class WeatherData:
    dt: datetime.datetime
    temperature: Temperature
    weathers: list[Weather]
    humidity: float
    rain_3h: float
    snow_3h: float

    @classmethod
    def from_response(cls, response: dict) -> WeatherData:
        rain_3h = 0
        snow_3h = 0

        if "rain" in response:
            rain_3h = float(response["rain"]["3h"])

        if "snow" in response:
            snow_3h = float(response["snow"]["3h"])

        return WeatherData(
            dt=datetime.datetime.strptime(response["dt_txt"], "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=zoneinfo.ZoneInfo("UTC")
            ),
            temperature=Temperature(
                avg=response["main"]["temp"],
                min=response["main"]["temp_min"],
                max=response["main"]["temp_max"],
                feels_like=response["main"]["feels_like"],
            ),
            weathers=[Weather.from_dict(w) for w in response["weather"]],
            humidity=response["main"]["humidity"],
            rain_3h=rain_3h,
            snow_3h=snow_3h,
        )
