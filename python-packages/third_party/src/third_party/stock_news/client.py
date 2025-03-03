from loguru import logger
import requests
from requests import exceptions

from . import config as stock_news_config

_BASE_URL = "https://stocknewsapi.com/api/v1/sundown-digest"


def get_latest_sundown_report(page: int = 1, items: int = 3) -> dict:
    config = stock_news_config.load_config()

    try:
        response = requests.get(
            _BASE_URL,
            params={
                "page": page,
                "token": config.api_key,
            },
        )
        return response.json()["data"][0]
    except exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}, Status Code: {response.status_code}")
