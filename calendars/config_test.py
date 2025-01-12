import os

import pytest

from calendars import config


@pytest.mark.parametrize(
    "email, calendar_id, token, refresh_token",
    [
        ("test_email_1", "test_calendar_id_1", "test_token_1", "test_refresh_token_1"),
        ("test_email_2", "test_calendar_id_2", "test_token_2", "test_refresh_token_2"),
    ],
)
def test_load_config(email: str, calendar_id: str, token: str, refresh_token: str):
    os.environ["GOOGLE_EMAIL"] = email
    os.environ["GOOGLE_CALENDAR_ID"] = calendar_id
    os.environ["GOOGLE_TOKEN"] = token
    os.environ["GOOGLE_REFRESH_TOKEN"] = refresh_token

    cfg = config.load_config()

    assert cfg.email == email
    assert cfg.calendar_id == calendar_id
    assert cfg.token == token
    assert cfg.refresh_token == refresh_token
