import datetime
import zoneinfo

from loguru import logger
from third_party.discord import client as discord
from third_party.discord import settings as discord_settings
from third_party.kakao import watcher
from third_party.openweather import client as openweather
from third_party.openweather import dto as openweather_dto

from utils import airports as airport_utils
from utils import times as time_utils


def _get_weather_data_of_interests(
    weathers: list[openweather_dto.WeatherData],
    arrival_time: datetime.datetime,
    leaving_time: datetime.datetime,
) -> list[openweather_dto.WeatherData]:
    return list(filter(lambda w: time_utils.is_between(w.dt, arrival_time, leaving_time), weathers))


def _get_weather_emoji(weather_main: str) -> str:
    if weather_main == "Clear":
        return "☀️"
    if weather_main == "Clouds":
        return "☁️"
    if weather_main == "Rain":
        return "🌧️"
    if weather_main == "Snow":
        return "❄️"
    if weather_main == "Wind":
        return "🌬️"
    return "❓"


@watcher.report_error
def main(
    arrival_airport: str,
    arrival_time: datetime.datetime,
    leaving_time: datetime.datetime,
    margin_hours: int = 3,
) -> None:
    """Check the weather of area around the airport from
    arrival_time - margin_hours to leaving_time + margin_hours and report to user.

    Args:
        arrival_airport (str): The name of airport that user will arrive.
        arrival_time (datetime.datetime): The time that user will arrive.
        leaving_time (datetime.datetime): The time that user will leave.
        margin_hours (int, optional): The margin hours that user want to check. Defaults to 3.
    """
    assert airport_utils.check_iata_code_exists(arrival_airport), f"Invalid airport code: {arrival_airport}"
    arrival_timezone = airport_utils.get_timezone_by_iata_code(arrival_airport)

    arrival_time = time_utils.to_timezone(arrival_time, arrival_timezone)
    leaving_time = time_utils.to_timezone(leaving_time, arrival_timezone)

    margined_arrival_time = time_utils.hours_before(arrival_time, margin_hours)
    margined_leaving_time = time_utils.hours_after(leaving_time, margin_hours)

    logger.info(f"Search for weather of {arrival_airport} from {margined_arrival_time} to {margined_leaving_time}")

    coordinate = airport_utils.get_coord_by_iata_code(arrival_airport)
    weathers = openweather.get_daily_weather(lat=coordinate.lat, lon=coordinate.lon)
    weathers_filtered = _get_weather_data_of_interests(weathers, margined_arrival_time, margined_leaving_time)

    notices = []
    for w in weathers_filtered:
        local_datetime = time_utils.to_timezone(w.dt, arrival_timezone)
        max_temp = int(w.temp.max)
        min_temp = int(w.temp.min)
        weather_main = w.weather[0].main

        notices.append(
            f"{time_utils.DateTimeFormatter.COMPACTDATE_KR.format(local_datetime)}: {_get_weather_emoji(weather_main)} ↓{min_temp:02d}℃ / ↑{max_temp:02d}℃"
        )

    logger.info(
        f"Generated weather report for {arrival_airport} from {margined_arrival_time} to {margined_leaving_time}"
    )
    summary = "\n".join(notices)
    discord.send_to_weather(
        message=(
            f"<@{discord_settings.ARIES_PIG}>님!\n"
            + f"**{time_utils.DateTimeFormatter.COMPACTDATE_KR.format(arrival_time)}**부터 **{time_utils.DateTimeFormatter.COMPACTDATE_KR.format(leaving_time)}**까지 **{airport_utils.get_cityname_by_iata_code(arrival_airport)}** 날씨 보고서를 가져왔어요🌡️\n"
            + "```\n"
            + f"{summary}"
            + "```"
        )
    )


if __name__ == "__main__":
    main(
        "LHR",
        datetime.datetime(2025, 3, 2, 12, 25, tzinfo=zoneinfo.ZoneInfo("Asia/Seoul")),
        datetime.datetime(2025, 3, 4, 5, 10, tzinfo=zoneinfo.ZoneInfo("Asia/Seoul")),
    )
