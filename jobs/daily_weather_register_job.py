from loguru import logger
from third_party.calendars import gcal
from third_party.kakao import client as kakaotalk

from jobs import monitor_weather
from scheduler import instance
from scheduler import jobs
from utils import airports as airport_utils
from utils import flights as flight_utils
from utils import times as time_utils

_SEARCH_WINDOW = 7


def _check_if_flight_schedule(event) -> bool:
    return len(event.summary) == 11 and "->" in event.summary


def _filter_events_of_interest(events: list) -> list:
    events_of_interests = []
    for e in events:
        if not _check_if_flight_schedule(e):
            continue

        chunks = e.summary.split("->")
        dep_iata = chunks[-2][1:4]
        arr_iata = chunks[-1][1:]

        if dep_iata not in ["ICN", "GMP"]:
            continue

        if airport_utils.get_timezone_by_iata_code(arr_iata) == time_utils.TimeZone.SEOUL.value:
            continue
        events_of_interests.append(e)
    return events_of_interests


def _search_return_flight_schedule(
    all_events: list,
    flight: flight_utils.Flight,
) -> flight_utils.Flight:
    logger.info(f"Searching return flight schedule for {flight}")

    for event in all_events:
        if not _check_if_flight_schedule(event):
            continue

        dep_iata, arr_iata = flight_utils.Flight.parse_summary(event.summary).values()
        if dep_iata != flight.arrival_airport:
            continue

        logger.info(f"Found return flight schedule: {event}")
        return flight_utils.Flight(
            departure_time=event.start,
            departure_airport=dep_iata,
            arrival_airport=arr_iata,
            arrival_time=event.end,
        )
    raise ValueError(f"Return flight schedule not found for {flight}")


@instance.DefaultBackgroundScheduler.scheduled_job(jobs.TriggerType.CRON, hour=00, minute=20)
def main():
    logger.debug("Registering weather monitering jobs...")
    today = time_utils.get_today_as_date()
    google_calendar_client = gcal.load_google_calendar_client()

    events = google_calendar_client.get_events(
        time_min=time_utils.get_start_of_the_day(time_utils.get_days_after(today, days=1)),
        time_max=time_utils.get_end_of_the_day(time_utils.get_days_after(today, days=2)),
    )

    all_events = google_calendar_client.get_events(
        time_min=time_utils.get_start_of_the_day(time_utils.get_days_after(today, days=1)),
        time_max=time_utils.get_end_of_the_day(time_utils.get_days_after(today, days=_SEARCH_WINDOW)),
    )

    weather_events = _filter_events_of_interest(events)
    logger.info(f"Events of interest: {weather_events}")
    weather_jobs = []
    summaries = []

    for event in weather_events:
        assert event.end, f"event.end must be set, but found {event}"

        dep_iata, arr_iata = flight_utils.Flight.parse_summary(event.summary).values()
        flight_event = flight_utils.Flight(
            departure_time=event.start,
            departure_airport=dep_iata,
            arrival_airport=arr_iata,
            arrival_time=event.end,
        )
        rt_flight_event = _search_return_flight_schedule(all_events, flight_event)
        weather_jobs.append(
            jobs.WeatherJob(
                func=monitor_weather.main,
                arrival_airport=arr_iata,
                arrival_time=flight_event.arrival_time,
                leaving_time=rt_flight_event.departure_time,
            ).add_ctx(
                trigger=jobs.TriggerType.DATE,
                next_run_time=time_utils.minutes_after(time_utils.now(), 5),
            )
        )
        summaries.append(f"- {flight_event.summary()}")

    for job in weather_jobs:
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

    summaries = "\n".join(summaries)
    kakaotalk.send_to_me(f"""
        {today} 날씨 모니터링 등록 완료
        대상: {time_utils.get_days_after(today, days=1)} ~ {time_utils.get_days_after(today, days=2)}
        일정: \n{summaries}
    """)
