import pytz

from apscheduler.schedulers import background
from cron import spec

DefaultBackgroundScheduler = background.BackgroundScheduler(
    job_defaults=spec.get_scheduler_args(),
    jobstores=spec.get_jobstores(),
    executors=spec.get_executor(),
    timezone=pytz.timezone("Asia/Seoul"),
)
