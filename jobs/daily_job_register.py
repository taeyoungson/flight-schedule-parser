from loguru import logger
from jobs import monitor_flights
from scheduler import instance
from scheduler import jobs
from third_party.calendars import gcal
from third_party.kakao import client as kakaotalk
from utils import times as time_utils


def _check_if_flight_schedule(event) -> bool:
    return len(event.summary) == 10 and "-" in event.summary


def _parse_kwargs_from_event(event) -> dict[str, str]:
    chunks = event.summary.split("->")

    dep_iata = chunks[-2][1:4]
    arr_iata = chunks[-1][1:]

    return {
        "dep_iata": dep_iata,
        "arr_iata": arr_iata,
    }


def _summarize_calendar_jobs(calendar_jobs: list[jobs.CalendarJob]) -> str:
    return "\n".join([f"{job.description}" for job in calendar_jobs])


@instance.DefaultBackgroundScheduler.scheduled_job(jobs.TriggerType.CRON, hour=0, minute=10)
def main():
    logger.debug("Registering daily jobs...")

    google_calendar_client = gcal.load_google_calendar_client()

    events_of_today = google_calendar_client.get_events(
        time_min=time_utils.get_start_of_the_day(time_utils.get_today_as_date()),
        time_max=time_utils.get_end_of_the_day(time_utils.get_today_as_date()),
    )

    flight_events = list(filter(lambda e: _check_if_flight_schedule(e), events_of_today))

    if not flight_events:
        logger.info(f"No flight schedule found {time_utils.get_today_as_date()}")
        kakaotalk.send_to_me(f"{time_utils.get_today_as_date()}\n오늘은 비행 스케쥴이 없네요!")
        return

    calendar_jobs = []
    for event in flight_events:
        assert event.end, f"event.end must be set, but found {event}"
        calendar_jobs.append(
            jobs.CalendarJob(
                func=monitor_flights.main,
                **_parse_kwargs_from_event(event),
            ).add_ctx(
                trigger=jobs.TriggerType.DATE,
                next_run_time=time_utils.minutes_before(event.end, minutes=20),
            )
        )

    for job in calendar_jobs:
        logger.debug(f"Registering job: {job.description}")
        instance.DefaultBackgroundScheduler.add_job(
            id=job.id,
            name=job.name,
            func=job.func,
            args=job.args,
            kwargs=job.kwargs,
            trigger=job.trigger,
            next_run_time=job.next_run_time,
        )

    # kakaotalk.send_to_me(f"{time_utils.get_today_as_date()}\n총 {len(calendar_jobs)}개의 조회 일정을 등록해 두었어요.")
    kakaotalk.send_to_me(f"""
        {time_utils.get_today_as_date()} 일정 등록 완료
        ---
        {_summarize_calendar_jobs(calendar_jobs)}
    """)
