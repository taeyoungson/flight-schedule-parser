import argparse
import base64
import io

import fastapi
from PIL import Image
import uvicorn

from jobs import parse_data_from_image
from server import dto

app = fastapi.FastAPI()


@app.post("/img")
def parse_schedule(req: dto.ImageData):
    img = Image.open(io.BytesIO(base64.b64decode(req.img_base64)))
    parse_data_from_image.get_flight_schedule(img)


def main(opts: argparse.Namespace):
    uvicorn.run("server.api:app", port=opts.port, host=opts.host)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8888)

    main(parser.parse_args())
