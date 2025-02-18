from loguru import logger
import requests
from requests import exceptions

from kakao import auth

_TIMEOUT = 10
_SEND_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"


def send_to_me(message: str) -> None:
    token = auth.get_authorization_token()
    try:
        response = requests.post(
            url=_SEND_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            },
            data={
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


send_to_me("hi")
