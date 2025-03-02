import datetime

import pytest_mock

from jobs import monitor_weather


def test_monitor_weathers(mocker: pytest_mock.MockFixture):
    mock_discord = mocker.patch("third_party.discord.client.send_to_weather")
    mock_filter_weathers = mocker.patch("jobs.monitor_weather._get_weather_data_of_interests")
    mock_get_daily_weather = mocker.patch("third_party.openweather.client.get_daily_weather", return_value=[])
    mock_openai_bot = mocker.patch("models.weather_bot.load_weather_bot")

    monitor_weather.main("ICN", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=2))

    mock_get_daily_weather.assert_called_once()
    mock_filter_weathers.assert_called_once()
    mock_openai_bot.assert_called_once()
    mock_discord.assert_called_once()
