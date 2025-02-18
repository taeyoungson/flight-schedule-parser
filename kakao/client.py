from loguru import logger
import pydantic
import pydantic_settings
import requests
from requests import exceptions

_SEND_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
_TIMEOUT = 10


class KakaoConfig(pydantic_settings.BaseSettings):
    api_key: str = pydantic.Field(...)
    redirect_uri: str = pydantic.Field(...)

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="KAKAO_",
        env_file=".env.dev",
        extra="allow",
    )


def _load_config() -> KakaoConfig:  # pylint: disable=no-value-for-parameter
    return KakaoConfig()


def _get_authorization_token() -> str:
    config = _load_config()

    try:
        response = requests.get(
            url=_AUTH_URL,
            params={
                "client_id": config.api_key,
                "redirect_uri": config.redirect_uri,
                "response_type": "code",
            },
            timeout=_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()["code"]

    except exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")


def send_to_me(message: str) -> None:
    config = _load_config()

    try:
        response = requests.post(
            url=_SEND_URL,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            },
            json={
                "template_object": {
                    "object_type": "text",
                    "text": message,
                    "link": {
                        "web_url": "https://developers.kakao.com",
                        "mobile_web_url": "https://developers.kakao.com",
                    },
                    "button_title": "바로 확인",
                },
            },
            timeout=_TIMEOUT,
        )
        response.raise_for_status()

    except exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")
    except exceptions.RequestException as err:
        logger.error(f"Request Error: {err}")
