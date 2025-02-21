import time
import jobs  # noqa: F401

from scheduler import instance
from loguru import logger


def main():
    sdler = instance.DefaultBackgroundScheduler
    sdler.start()

    try:
        while True:
            sdler.print_jobs()
            time.sleep(10)
    except KeyboardInterrupt:
        logger.debug("Exitting...")
        sdler.shutdown()


if __name__ == "__main__":
    main()
