from __future__ import annotations

import dataclasses
import datetime
import zoneinfo


@dataclasses.dataclass
class Temperature:
    max: float
    min: float


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
    temp: Temperature
    weather: list[Weather]
    humidity: float
    rain: float
    snow: float
    uvi: float

    @classmethod
    def from_response(cls, daily_response: dict) -> WeatherData:
        rain = 0
        snow = 0

        if "rain" in daily_response:
            rain = float(daily_response["rain"])

        if "snow" in daily_response:
            snow = float(daily_response["snow"])

        return WeatherData(
            dt=datetime.datetime.fromtimestamp(daily_response["dt"]).replace(tzinfo=zoneinfo.ZoneInfo("UTC")),
            temp=Temperature(
                min=daily_response["temp"]["min"],
                max=daily_response["temp"]["max"],
            ),
            weather=[Weather.from_dict(w) for w in daily_response["weather"]],
            humidity=daily_response["humidity"],
            uvi=daily_response["uvi"],
            rain=rain,
            snow=snow,
        )
