import json
import textwrap

from loguru import logger
import requests

from . import config as discord_config


def send_to_dev(message: str, image_url: str | None = None) -> None:
    config = discord_config.load_config()
    embeds = []

    if not config.dev_webhook:
        logger.warning("discord dev_webhook is not set. Skip sending message to dev.")
        return

    if image_url:
        embeds = [{"image": {"url": image_url}}]

    try:
        response = requests.post(
            url=config.dev_webhook,
            data=json.dumps(
                {
                    "content": textwrap.dedent(message),
                    "embeds": embeds,
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Failed to send message to dev: {e}") from e


def send_to_weather(message: str, image_url: str | None = None) -> None:
    config = discord_config.load_config()
    embeds = []

    if not config.weather_webhook:
        logger.warning("discord weather_webhook is not set. Skip sending message to dev.")
        return

    if image_url:
        embeds = [{"image": {"url": image_url}}]

    try:
        response = requests.post(
            url=config.weather_webhook,
            data=json.dumps(
                {
                    "content": textwrap.dedent(message),
                    "embeds": embeds,
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Failed to send message to dev: {e}") from e


def send_to_flight(message: str, image_url: str | None = None) -> None:
    config = discord_config.load_config()
    embeds = []

    if not config.flight_webhook:
        logger.warning("discord flight_webhook is not set. Skip sending message to dev.")
        return

    if image_url:
        embeds = [{"image": {"url": image_url}}]

    try:
        response = requests.post(
            url=config.flight_webhook,
            data=json.dumps(
                {
                    "content": textwrap.dedent(message),
                    "embeds": embeds,
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Failed to send message to dev: {e}") from e
