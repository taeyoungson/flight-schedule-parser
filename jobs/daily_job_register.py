import datetime
from loguru import logger
from jobs import monitor_flights
from cron import instance
from cron import jobs


# @instance.DefaultBackgroundScheduler.scheduled_job(jobs.TriggerType.CRON, minute=53)
def main():
    logger.debug("Registering daily jobs...")
    dummy_gcal_data = [
        {
            "dep_iata": "NGO",
            "arr_iata": "ICN",
            "arrive_at": datetime.datetime(2025, 2, 21, 19, 25),
        }
    ]

    calendar_jobs = []
    for kwargs in dummy_gcal_data:
        calendar_jobs.append(
            jobs.BaseJob(
                func=monitor_flights.main,
                trigger_type=jobs.TriggerType.DATE,
                func_kwargs=kwargs,
            )
        )

    for job in calendar_jobs:
        logger.debug(f"Registering job: {job.description}")
        instance.DefaultBackgroundScheduler.add_job(
            id=job.id,
            name=job.name,
            func=job.func,
            args=job.func_args,
            kwargs=job.func_kwargs,
            trigger=job.trigger,
            next_run_time=job.func_kwargs["arrive_at"],
        )

    instance.DefaultBackgroundScheduler.start()

    import time

    try:
        while True:
            instance.DefaultBackgroundScheduler.print_jobs()
            time.sleep(10)
    except KeyboardInterrupt:
        logger.debug("Exitting...")
        instance.DefaultBackgroundScheduler.shutdown()


if __name__ == "__main__":
    main()
