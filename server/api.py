import argparse

import fastapi
import mangum
import uvicorn

from scheduler import instance
from jobs import parse_flight_ocr_result
from server import dto

app = fastapi.FastAPI()
handler = mangum.Mangum(app)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/jobs")
def jobs():
    instance.DefaultBackgroundScheduler.print_jobs()
    return {"jobs": instance.DefaultBackgroundScheduler.get_jobs()}


@app.post("/register/flight")
def parse(req: dto.RegisterFlightRequest):
    parse_flight_ocr_result.build_flight_schedule(raw_ocr_result=req.raw_ocr_result, year=req.year, month=req.month)


def main(opts: argparse.Namespace):
    instance.DefaultBackgroundScheduler.start()
    uvicorn.run(
        "server.api:app", host=opts.host, port=opts.port, ssl_keyfile=opts.ssl_keyfile, ssl_certfile=opts.ssl_certfile
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--ssl-keyfile", type=str, required=True)
    parser.add_argument("--ssl-certfile", type=str, required=True)

    main(parser.parse_args())
