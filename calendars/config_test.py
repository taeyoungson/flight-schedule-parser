import os

import pytest

from calendars import config


@pytest.mark.parametrize(
    "email, calendar_id",
    [
        ("test_email_1", "test_calendar_id_1"),
        ("test_email_2", "test_calendar_id_2"),
    ],
)
def test_load_config(email: str, calendar_id: str):
    os.environ["GOOGLE_EMAIL"] = email
    os.environ["GOOGLE_CALENDAR_ID"] = calendar_id
    cfg = config.load_config()
    assert cfg.email == email
    assert cfg.calendar_id == calendar_id
