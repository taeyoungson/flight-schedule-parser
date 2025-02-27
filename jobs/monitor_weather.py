import datetime

from loguru import logger
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns
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


@watcher.report_error
def main(
    arrive_airport: str,
    arrival_time: datetime.datetime,
    leaving_time: datetime.datetime,
    margin_hours: int = 3,
) -> None:
    """Check the weather of area aroun the airport from
    arrival_time - margin_hours to leaving_time + margin_hours and report to user.

    Args:
        arrive_airport (str): The name of airport that user will arrive.
        arrival_time (datetime.datetime): The time that user will arrive.
        leaving_time (datetime.datetime): The time that user will leave.
    """
    assert airport_utils.check_iata_code_exists(arrive_airport), f"Invalid airport code: {arrive_airport}"

    margined_arrival_time = time_utils.hours_before(arrival_time, margin_hours)
    margined_leaving_time = time_utils.hours_after(leaving_time, margin_hours)

    logger.info(f"Search for weather of {arrive_airport} from {margined_arrival_time} to {margined_leaving_time}")

    coordinate = airport_utils.get_coord_by_iata_code(arrive_airport)
    weathers = openweather.get_weather_by_coord(lat=coordinate.lat, lon=coordinate.lon)
    weathers_filtered = _get_weather_data_of_interests(weathers, margined_arrival_time, margined_leaving_time)

    # plot data
    dates = []
    avg_temps = []
    max_temps = []
    min_temps = []
    for w in weathers_filtered:
        dates.append(time_utils.to_timezone(w.dt, time_utils.TimeZone.SEOUL.value))
        avg_temps.append(w.temperature.avg)
        max_temps.append(w.temperature.max)
        min_temps.append(w.temperature.min)

    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    mpl.rc("font", family="AppleGothic")

    plt.axvline(x=arrival_time, color="green", linestyle="dashed")
    plt.text(
        arrival_time,
        plt.ylim()[1] * 0.95,
        "출발",
        ha="center",
        va="top",
        fontsize=10,
        fontweight="bold",
        color="black",
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"),
    )

    plt.axvline(x=leaving_time, color="green", linestyle="dashed")
    plt.text(leaving_time, plt.ylim()[1] + 1, "출발", ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.fill_between(dates, avg_temps, max_temps, color="red", alpha=0.1)
    plt.fill_between(dates, min_temps, avg_temps, color="blue", alpha=0.1)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d일 %H시"))

    sns.lineplot(x=dates, y=max_temps, label="최고 기온", color="red", linestyle="dashed")
    sns.lineplot(x=dates, y=min_temps, label="최저 기온", color="blue", linestyle="dashed")
    sns.lineplot(x=dates, y=avg_temps, label="평균 기온", color="black", linewidth=2)

    # show
    plt.show()


if __name__ == "__main__":
    main(
        "ICN",
        (time_utils.now() + datetime.timedelta(days=1, hours=0)),
        (time_utils.now() + datetime.timedelta(days=1, hours=72)),
    )
