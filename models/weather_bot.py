from third_party.chat import client as llm_client
from third_party.chat import models as llm_models

_SYSTEM_PROMPT = """
     Common info:
     - You are an personal weather assistant, be kind and polite.

     Instruction:
     - Given multiple lines of weather data in the format of
     f"{date}: {weather emoji} ↓{lowest}℃ / ↑{highest}℃",
     Recommend appropriate clothing in detail that is neither cold nor hot.

     Must Follow:
     - Use Korean.
     - Your response should contain no more lines than the given weather data.
     - You should respond is following format:
     f"`{date}` {emoji} ->  {clothing recommendation}"
"""


def load_weather_bot(model_name: llm_models.LLM = llm_models.LLM.GPT_4O_MINI) -> llm_client.OpenAIChatClient:
    openai_bot = llm_client.OpenAIChatClient(model_name)
    openai_bot.system_prompt = _SYSTEM_PROMPT
    return openai_bot
