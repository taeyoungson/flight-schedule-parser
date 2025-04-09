import discord
from discord import message as discord_message
from loguru import logger
from third_party.chat import client as llm_client
from third_party.chat import models as llm_models

from bots.discord import base
from bots.discord import config


def _get_llm_answer_agent(model_name: llm_models.LLM = llm_models.LLM.GPT_4O_MINI) -> llm_client.OpenAIChatClient:
    openai_bot = llm_client.OpenAIChatClient(model_name)
    openai_bot.system_prompt = """
    Common info:
    - You are an personal assistant in Discord, named Jarvis, please be kind and polite.
    - You answer questions and provide information to users in Discord.
    """
    return openai_bot


class JarvisDiscordBot(base.DiscordChatBot):
    _llm_agent: llm_client.OpenAIChatClient = _get_llm_answer_agent()

    async def on_message(self, message: discord_message.Message):
        if message.author == self.user:
            return

        logger.debug(f"Received message: {message.content}")

        if self._is_mentioned(message):
            message.content = self._remove_mention(message)
            history = await self._build_message_history(message)

            logger.debug(f"Message history: {history}")
            response = await self._llm_agent.ainvoke(history)
            await message.channel.send(response.content)

        else:
            logger.debug("Message not mentioned to Jarvis, ignoring.")


if __name__ == "__main__":
    logger.info("Starting Jarvis Discord Bot")

    intents = discord.Intents.default()
    intents.message_content = True

    jarvis_bot = JarvisDiscordBot(intents=intents)
    jarvis_bot_config = config.load_config()
    jarvis_bot.run(jarvis_bot_config.jarvis_bot_token)
