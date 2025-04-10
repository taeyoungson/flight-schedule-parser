import abc

from langchain import chat_models
from langchain_core import messages
import overrides

from . import config as llm_config
from . import models as llm_models


class BaseChatClient(abc.ABC):
    _system_prompt: str
    _model_provider: str

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, prompt: str) -> str:
        self._system_prompt = prompt

    @abc.abstractmethod
    def invoke(self, message: str) -> messages.AIMessage:
        pass

    @abc.abstractmethod
    def ainvoke(self, message: str) -> messages.AIMessage:
        pass


class OpenAIChatClient(BaseChatClient):
    _system_prompt: str
    _model_provider: str = llm_models.Provider.OPENAI

    def __init__(self, model_name: llm_models.LLM, tools: list):
        self._config = llm_config.load_config()
        self._model = chat_models.init_chat_model(
            model=f"{self._model_provider}:{model_name.value}",
            api_key=self._config.openai_api_key,
        )
        self._model_with_tools = None

        if len(tools) > 0:
            self._model_with_tools = self._model.bind_tools(tools)

    @overrides.override
    def invoke(self, message: str | list[str]) -> messages.AIMessage:
        if isinstance(message, str):
            message = [message]
        return self._model.invoke(
            [
                messages.SystemMessage(self._system_prompt),
            ]
            + [messages.HumanMessage(msg) for msg in message],
        )

    @overrides.override
    def ainvoke(self, message: str | list[str], tool_message: list | None = None) -> messages.AIMessage:
        if isinstance(message, str):
            message = [message]

        if tool_message is None:
            tool_message = []

        return self._model.ainvoke(
            [messages.SystemMessage(self._system_prompt)]
            + [messages.HumanMessage(msg) for msg in message]
            + tool_message
        )

    def invoke_tools(self, message: str | list[str]) -> messages.AIMessage:
        if not self._model_with_tools:
            raise ValueError("No tools provided")

        return self._model_with_tools.invoke(
            [messages.SystemMessage(self._system_prompt)] + [messages.HumanMessage(msg) for msg in message],
        )
