import datetime
import tempfile
import zoneinfo

from loguru import logger
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import seaborn as sns
from third_party.discord import client as discord
from third_party.imgbb import client as imgbb
from third_party.kakao import watcher
from third_party.openweather import client as openweather
from third_party.openweather import dto as openweather_dto

from utils import airports as airport_utils
from utils import times as time_utils

mpl.rc("font", family="NanumGothic")


def _get_weather_data_of_interests(
    weathers: list[openweather_dto.WeatherData],
    arrival_time: datetime.datetime,
    leaving_time: datetime.datetime,
) -> list[openweather_dto.WeatherData]:
    return list(filter(lambda w: time_utils.is_between(w.dt, arrival_time, leaving_time), weathers))


def _build_weather_report(
    weathers: list[openweather_dto.WeatherData],
    arrive_airport: str,
    arrival_time: datetime.datetime,
    leaving_time: datetime.datetime,
    tz: zoneinfo.ZoneInfo,
) -> None:
    dates = []
    avg_temps = []
    max_temps = []
    min_temps = []
    rains = []
    snows = []
    for w in weathers:
        dates.append(time_utils.to_timezone(w.dt, tz))
        avg_temps.append(w.temperature.avg)
        max_temps.append(w.temperature.max)
        min_temps.append(w.temperature.min)
        rains.append(w.rain_3h)
        snows.append(w.snow_3h)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    unique_dates = sorted(list(set([d.date() for d in dates])))
    for date in unique_dates:
        ax1.axvline(x=date, color="gray", linestyle="--", alpha=0.2)

    sns.lineplot(x=dates, y=max_temps, label="최고 기온", color="red", linestyle="dashed", ax=ax1)
    sns.lineplot(x=dates, y=min_temps, label="최저 기온", color="blue", linestyle="dashed", ax=ax1)
    sns.lineplot(x=dates, y=avg_temps, label="평균 기온", color="black", linewidth=2, ax=ax1)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d일 %H시"))

    ax1.axvline(x=arrival_time, color="green", linestyle="--")
    ax1.text(
        arrival_time,
        ax1.get_ylim()[1] * 0.9,
        "착륙",
        ha="center",
        va="top",
        fontsize=20,
        color="#E30613",
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"),
        fontproperties=fm.FontProperties(family="Segoe UI Emoji"),
    )

    ax1.axvline(x=leaving_time, color="green", linestyle="--")
    ax1.text(
        leaving_time,
        ax1.get_ylim()[1] * 0.9,
        "이륙",
        ha="center",
        va="top",
        fontsize=20,
        color="#E30613",
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"),
        # fontproperties=fm.FontProperties(family="Segoe UI Emoji"),
    )

    ax1.fill_between(dates, avg_temps, max_temps, color="red", alpha=0.1)
    ax1.fill_between(dates, min_temps, avg_temps, color="blue", alpha=0.1)

    ax2 = ax1.twinx()
    ax2.bar(dates, rains, color="blue", alpha=0.6, width=0.05, label="강수량 (mm)")
    ax2.set_ylabel("강수량 (mm)", color="black")
    ax2.tick_params(axis="y", labelcolor="black")
    ax2.set_ylim(0, 20)

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.title(f"{arrive_airport} ({unique_dates[0]} - {unique_dates[-1]})", fontsize=15)


@watcher.report_error
def main(
    arrive_airport: str,
    arrival_time: datetime.datetime,
    leaving_time: datetime.datetime,
    margin_hours: int = 3,
) -> None:
    """Check the weather of area around the airport from
    arrival_time - margin_hours to leaving_time + margin_hours and report to user.

    Args:
        arrive_airport (str): The name of airport that user will arrive.
        arrival_time (datetime.datetime): The time that user will arrive.
        leaving_time (datetime.datetime): The time that user will leave.
        margin_hours (int, optional): The margin hours that user want to check. Defaults to 3.
    """
    assert airport_utils.check_iata_code_exists(arrive_airport), f"Invalid airport code: {arrive_airport}"

    margined_arrival_time = time_utils.hours_before(arrival_time, margin_hours)
    margined_leaving_time = time_utils.hours_after(leaving_time, margin_hours)

    logger.info(f"Search for weather of {arrive_airport} from {margined_arrival_time} to {margined_leaving_time}")

    coordinate = airport_utils.get_coord_by_iata_code(arrive_airport)
    weathers = openweather.get_weather_by_coord(lat=coordinate.lat, lon=coordinate.lon)
    weathers_filtered = _get_weather_data_of_interests(weathers, margined_arrival_time, margined_leaving_time)

    _build_weather_report(
        weathers_filtered,
        arrive_airport,
        arrival_time,
        leaving_time,
        airport_utils.get_timezone_by_iata_code(arrive_airport),
    )

    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        plt.savefig(f.name)
        img_url = imgbb.upload_image(f.name)
    logger.info(
        f"Generated weather report for {arrive_airport} from {margined_arrival_time} to {margined_leaving_time}"
    )
    logger.info(f"Image URL: {img_url}")

    discord.send_to_dev(
        message=f"""
            조사일: **{arrival_time.strftime("%m월 %d일")}**
            지역: **{airport_utils.get_cityname_by_iata_code(arrive_airport)} 날씨 보고서**
            대상 시간: **{arrival_time.strftime("%m월 %d일 %H시")} ~ {leaving_time.strftime("%m월 %d일 %H시")}**
        """,
        image_url=img_url,
    )
