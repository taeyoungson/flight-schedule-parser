import json
import textwrap

from loguru import logger
import requests
from requests import exceptions

from . import auth

_TIMEOUT = 10
_SEND_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"


def _dedent_text(message: str) -> str:
    return textwrap.dedent(message)


def send_to_me(message: str) -> None:
    try:
        token = auth.get_authorization_token()
        response = requests.post(
            url=_SEND_URL,
            headers={
                "Authorization": f"Bearer {token['access_token']}",
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            },
            data={
                "template_object": json.dumps(
                    {
                        "object_type": "text",
                        "text": _dedent_text(message),
                        "link": None,
                    }
                ),
            },
            timeout=_TIMEOUT,
        )
        response.raise_for_status()

    except exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")
    except exceptions.RequestException as err:
        logger.error(f"Request Error: {err}")
