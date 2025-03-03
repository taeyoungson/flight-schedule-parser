import json
import textwrap

from loguru import logger
import requests

from . import config as discord_config


def _send(message: str, webhook: str, image_url: str | None = None) -> None:
    embeds = []

    if not webhook:
        logger.warning("discord webhook is not set. Skip sending message.")
        return

    if image_url:
        embeds = [{"image": {"url": image_url}}]

    try:
        response = requests.post(
            url=webhook,
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
        raise RuntimeError(f"Failed to send message: {e}") from e


def send_to_dev(message: str, image_url: str | None = None) -> None:
    config = discord_config.load_config()

    if not config.dev_webhook:
        logger.warning("discord dev_webhook is not set. Skip sending message to dev.")
        return

    return _send(message, config.dev_webhook, image_url)


def send_to_weather(message: str, image_url: str | None = None) -> None:
    config = discord_config.load_config()

    if not config.weather_webhook:
        logger.warning("discord dev_webhook is not set. Skip sending message to weather.")
        return

    return _send(message, config.weather_webhook, image_url)


def send_to_flight(message: str, image_url: str | None = None) -> None:
    config = discord_config.load_config()

    if not config.flight_webhook:
        logger.warning("discord schedule__webhook is not set. Skip sending message to flight.")
        return

    return _send(message, config.flight_webhook, image_url)


def send_to_finance(message: str, image_url: str | None = None) -> None:
    config = discord_config.load_config()

    if not config.finance_webhook:
        logger.warning("discord finance_webhook is not set. Skip sending message to finance.")
        return

    return _send(message, config.finance_webhook, image_url)
