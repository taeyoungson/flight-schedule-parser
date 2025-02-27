import base64

import requests

from . import config as img_bb_config

_UPLOAD_URL = "https://api.imgbb.com/1/upload"
_EXPIRATION = 60 * 60 * 24 * 30  # 30 days


def _open_image_and_encode_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def upload_image(image_path: str) -> str:
    config = img_bb_config.load_config()
    img_bas64 = _open_image_and_encode_base64(image_path)

    try:
        response = requests.post(
            url=_UPLOAD_URL,
            data={
                "key": config.api_key,
                "image": img_bas64,
                "expiration": _EXPIRATION,
            },
        )
        response.raise_for_status()
        return response.json()["data"]["url"]
    except Exception as e:
        raise RuntimeError(f"Failed to upload image: {e}") from e
