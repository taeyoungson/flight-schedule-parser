from __future__ import annotations

import datetime
import enum
from typing import Callable


class TriggerType(enum.StrEnum):
    CRON = "cron"
    DATE = "date"
    INTERVAL = "interval"


class TriggerMixin:
    def __init__(self):
        self._trigger_type = None
        self._next_run_at = None

    def add_ctx(self, trigger: TriggerType, next_run_time: datetime.datetime) -> TriggerMixin:
        self._trigger = trigger
        self._next_run_time = next_run_time

        return self

    @property
    def trigger(self) -> str:
        assert self._trigger, "Trigger Type is not set"
        return self._trigger.value

    @property
    def next_run_time(self) -> datetime.datetime:
        if not self._next_run_time:
            raise ValueError("next_run_at_ not set")
        return self._next_run_time


class BaseJob:
    def __init__(self, func: Callable, *args, **kwargs):
        self.func = func
        self._args = args
        self._kwargs = kwargs

    @property
    def id(self) -> str:
        return f"{self.func.__module__}.{self.func.__name__}.{self._kwargs.values()}"

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def description(self) -> str:
        return f"Function {self.id} with kwargs {self.kwargs}, trigger {self.trigger} at {self.next_run_time}"

    @property
    def name(self) -> str:
        return self.id


class CalendarJob(BaseJob, TriggerMixin):
    pass
