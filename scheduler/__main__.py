import jobs  # noqa: F401
import time
from loguru import logger

from scheduler import instance


def main():
    sdler = instance.DefaultBackgroundScheduler
    sdler.start()

    prev_jobs = None
    try:
        while True:
            time.sleep(60)
            current_jobs = sdler.get_jobs()
            if current_jobs != prev_jobs:
                prev_jobs = current_jobs
                sdler.print_jobs()

            else:
                continue
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt accepted")


if __name__ == "__main__":
    main()
