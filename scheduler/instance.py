import pytz

from loguru import logger
from apscheduler.schedulers import background
from scheduler import spec
from apscheduler import events
from third_party.kakao import client as kakaotalk


def _crash_report(event: events.JobEvent):
    kakaotalk.send_to_me(f"Job {event.job_id} crashed with exception: {event.jobstore}")


def _heartbeat() -> None:
    logger.info("Hearbeat heard")


DefaultBackgroundScheduler = background.BackgroundScheduler(
    job_defaults=spec.get_scheduler_args(),
    jobstores=spec.get_jobstores(),
    executors=spec.get_executor(),
    timezone=pytz.timezone("Asia/Seoul"),
)


DefaultBackgroundScheduler.add_job(_heartbeat, "interval", minutes=10)
DefaultBackgroundScheduler.add_listener(_crash_report, events.EVENT_JOB_ERROR)
