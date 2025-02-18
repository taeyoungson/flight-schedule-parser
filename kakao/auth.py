import json
import os

from loguru import logger
import requests
from requests import exceptions

from kakao import config as kakao_config

_TIMEOUT = 10
_AUTH_URL = "https://kauth.kakao.com/oauth/token"
_AUTH_INFO_URL = "https://kapi.kakao.com/v1/user/access_token_info"
_JSON_TOKEN_FILEPATH = "kakao_token.json"


def _validate_token(token: dict[str, str]) -> bool:
    try:
        response = requests.get(
            url=_AUTH_INFO_URL,
            headers={"Authorization": f"Bearer {token['access_token']}"},
            timeout=_TIMEOUT,
        )
        response.raise_for_status()

        return response.status_code == 200
    except exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")
        raise errh


def get_authorization_token() -> str:
    if os.path.exists(_JSON_TOKEN_FILEPATH):
        with open(_JSON_TOKEN_FILEPATH, mode="r", encoding="utf-8") as fp:
            token = json.load(fp)
        if _validate_token(token):
            return token

    config = kakao_config.load_config()

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
        raise errh
