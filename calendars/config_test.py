import os

import pytest

from calendars import config


@pytest.mark.parametrize(
    "email, calendar_id, token, token_uri, client_id, client_secret, refresh_token",
    [
        (
            "test_email_1",
            "test_calendar_id_1",
            "test_token_1",
            "test_token_uri_1",
            "test_client_id_1",
            "test_client_secret_1",
            "test_refresh_token_1",
        ),
        (
            "test_email_2",
            "test_calendar_id_2",
            "test_token_2",
            "test_token_uri_2",
            "test_client_id_2",
            "test_client_secret_2",
            "test_refresh_token_2",
        ),
    ],
)
def test_load_config(
    email: str, calendar_id: str, token: str, token_uri: str, client_id: str, client_secret: str, refresh_token: str
):
    os.environ["GOOGLE_EMAIL"] = email
    os.environ["GOOGLE_CALENDAR_ID"] = calendar_id
    os.environ["GOOGLE_TOKEN"] = token
    os.environ["GOOGLE_TOKEN_URI"] = token_uri
    os.environ["GOOGLE_CLIENT_ID"] = client_id
    os.environ["GOOGLE_CLIENT_SECRET"] = client_secret
    os.environ["GOOGLE_REFRESH_TOKEN"] = refresh_token

    cfg = config.load_config()

    assert cfg.email == email
    assert cfg.calendar_id == calendar_id
    assert cfg.token == token
    assert cfg.token_uri == token_uri
    assert cfg.client_id == client_id
    assert cfg.client_secret == client_secret
    assert cfg.refresh_token == refresh_token
