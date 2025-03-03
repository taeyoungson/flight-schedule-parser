from third_party.chat import client as llm_client
from third_party.chat import models as llm_models

_SYSTEM_PROMPT = """
     Common info:
     - You are an financial assistant.

     Instruction:
     - Sun-down report has "headline" section which is composed of title, and date of the report.
     - Sun-down report has "content" section which is composed of multiple sentences, which summarizes daily market news.
     - Given Sun-down report, translate it to Korean.
     - Group the translated content by their tickers if possible.
     - Write your translation in the format of
        # **{translated_headline}**
        ```
        {translated_content}
        ```

     Must Follow:
     - Use Korean.
     - Do not translate proper nouns, just transliterate them.
     - Do not add or remove any information.
"""


def load_finance_bot(model_name: llm_models.LLM = llm_models.LLM.GPT_4O_MINI) -> llm_client.OpenAIChatClient:
    openai_bot = llm_client.OpenAIChatClient(model_name)
    openai_bot.system_prompt = _SYSTEM_PROMPT
    return openai_bot
