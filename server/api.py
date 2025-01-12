import argparse

import fastapi
import mangum
import uvicorn

from jobs import parse_data_from_image
from server import dto

app = fastapi.FastAPI()
handler = mangum.Mangum(app)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/schedule")
def parse_schedule(req: dto.ScheduleData):
    parse_data_from_image.get_flight_schedule(req.result)


def main(opts: argparse.Namespace):
    uvicorn.run("server.api:app", host=opts.host, port=opts.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8888)

    main(parser.parse_args())
