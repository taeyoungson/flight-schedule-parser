import json
import os

from loguru import logger
import requests
from requests import exceptions

from . import config as kakao_config

_TIMEOUT = 10
_AUTH_CODEURL = "https://kauth.kakao.com/oauth/authorize"
_AUTH_URL = "https://kauth.kakao.com/oauth/token"
_AUTH_INFO_URL = "https://kapi.kakao.com/v1/user/access_token_info"
_JSON_TOKEN_FILEPATH = os.path.join(os.path.dirname(__file__), "kakao_token.json")


def _validate_token(token: dict[str, str]) -> bool:
    response = requests.get(
        url=_AUTH_INFO_URL,
        headers={"Authorization": f"Bearer {token['access_token']}"},
        timeout=_TIMEOUT,
    )

    return response.status_code == 200


def _print_get_code_url():
    config = kakao_config.load_config()

    response = requests.get(
        url=_AUTH_CODEURL,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
        params={
            "client_id": config.api_key,
            "redirect_uri": config.redirect_uri,
            "response_type": "code",
        },
        timeout=_TIMEOUT,
        allow_redirects=False,
    )

    assert response.status_code == 302

    redirect_uri = response.headers["Location"]
    logger.info(f"Open the following URL in your browser and authorize the app: {redirect_uri}")


def _refresh_auth_token(original_token: dict[str, str]) -> dict[str, str]:
    config = kakao_config.load_config()

    try:
        response = requests.post(
            url=_AUTH_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
            data={
                "grant_type": "refresh_token",
                "client_id": config.api_key,
                "refresh_token": original_token["refresh_token"],
            },
            timeout=_TIMEOUT,
        )
        response.raise_for_status()
        refreshed_token = response.json()

        if "refresh_token" not in refreshed_token:
            refreshed_token["refresh_token"] = original_token["refresh_token"]
            refreshed_token["refresh_token_expires_in"] = original_token["refresh_token_expires_in"]
        return refreshed_token

    except exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")
        raise errh


def get_authorization_token() -> dict[str, str]:
    config = kakao_config.load_config()

    # auth code not provided
    if not getattr(config, "auth_code", None):
        _print_get_code_url()
        raise ValueError("Authorization code is not set")

    # token file exists
    if os.path.exists(_JSON_TOKEN_FILEPATH):
        with open(_JSON_TOKEN_FILEPATH, mode="r", encoding="utf-8") as fp:
            token = json.load(fp)
        # token is valid
        if _validate_token(token):
            return token
        # token is invalid
        else:
            refreshed_token = _refresh_auth_token(original_token=token)
            with open(_JSON_TOKEN_FILEPATH, mode="w", encoding="utf-8") as fp:
                json.dump(refreshed_token, fp)
            return refreshed_token

    # token file does not exist, generate a new one
    else:
        try:
            response = requests.post(
                url=_AUTH_URL,
                headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": config.api_key,
                    "redirect_uri": config.redirect_uri,
                    "code": config.auth_code,
                },
                timeout=_TIMEOUT,
            )
            response.raise_for_status()
            token = response.json()

            with open(_JSON_TOKEN_FILEPATH, mode="w", encoding="utf-8") as fp:
                json.dump(token, fp)

            return token

        except exceptions.HTTPError as errh:
            logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")
            logger.error("Maybe the authorization code is invalid, please refresh the code if this error persists")
            raise errh
