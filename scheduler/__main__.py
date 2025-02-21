import time
import jobs  # noqa: F401

from scheduler import instance
from loguru import logger


def main():
    sdler = instance.DefaultBackgroundScheduler
    sdler.start()

    prev_jobs = None

    try:
        while True:
            current_jobs = sdler.get_jobs()
            if not current_jobs == prev_jobs:
                sdler.print_jobs()
                prev_jobs = current_jobs
            time.sleep(10)
    except KeyboardInterrupt:
        logger.debug("Exitting...")
        sdler.shutdown()


if __name__ == "__main__":
    main()
