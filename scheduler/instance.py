import pytz

from apscheduler.schedulers import background
from scheduler import spec
from apscheduler import events
from third_party.kakao import client as kakaotalk


def _crash_report(event: events.JobEvent):
    kakaotalk.send_to_me(f"Job {event.job_id} crashed with exception: {event.jobstore}")


DefaultBlockingScheduler = background.BlockingScheduler(
    job_defaults=spec.get_scheduler_args(),
    jobstores=spec.get_jobstores(),
    executors=spec.get_executor(),
    timezone=pytz.timezone("Asia/Seoul"),
)


DefaultBlockingScheduler.add_listener(_crash_report, events.EVENT_JOB_ERROR)
