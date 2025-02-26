import argparse

import fastapi
import mangum
import uvicorn

from jobs import parse_flight_ocr_result
from server import dto

app = fastapi.FastAPI()
handler = mangum.Mangum(app)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/register/flight")
def parse(req: dto.RegisterFlightRequest):
    parse_flight_ocr_result.build_flight_schedule(raw_ocr_result=req.raw_ocr_result, year=req.year, month=req.month)


def main(opts: argparse.Namespace):
    uvicorn.run("server.api:app", host=opts.host, port=opts.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8888)

    main(parser.parse_args())
