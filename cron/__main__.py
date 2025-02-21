import time
from apscheduler import events

from apscheduler.schedulers import base
from cron import jobs
from cron import instance
from loguru import logger
from third_party.kakao import client as kakao_client


def _crash_report(event: events.JobEvent):
    kakao_client.send_to_me(f"Job {event.job_id} crashed with exception: {event.jobstore}")


def _register_listeners(scheduler: base.BaseScheduler):
    scheduler.add_listener(_crash_report, events.EVENT_JOB_ERROR)


def main():
    scheduler = instance.DefaultBackgroundScheduler
    scheduler.start()
    _register_listeners(scheduler)

    try:
        while True:
            scheduler.print_jobs()
            time.sleep(10)
    except KeyboardInterrupt:
        logger.debug("Exitting...")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
