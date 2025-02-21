import enum
from typing import Callable


class TriggerType(enum.StrEnum):
    CRON = "cron"
    DATE = "date"
    INTERVAL = "interval"


class BaseJob:
    def __init__(
        self,
        func: Callable,
        func_args: tuple | None = None,
        func_kwargs: dict | None = None,
        trigger_type: TriggerType = TriggerType.DATE,
        trigger_kwargs: dict | None = None,
    ):
        self.func = func
        self.trigger_type = trigger_type

        self._func_args = func_args
        self._func_kwargs = func_kwargs
        self._trigger_kwargs = trigger_kwargs

    @property
    def id(self) -> str:
        return f"{self.func.__module__}.{self.func.__name__}"

    @property
    def func_args(self):
        return self._func_args

    @property
    def func_kwargs(self):
        return self._func_kwargs

    @property
    def trigger_kwargs(self):
        return self._trigger_kwargs

    @property
    def trigger(self) -> str:
        return self.trigger_type.value

    @property
    def description(self) -> str:
        return f"Function {self.id} with kwargs {self.func_kwargs}, Trigger {self.trigger} - {self.trigger_kwargs}"

    @property
    def name(self) -> str:
        return self.id
