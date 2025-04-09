import abc
import re

import discord
from discord import channel as discord_channel
from discord import message as discord_message
from discord import threads as discord_threads


class DiscordChatBot(discord.Client, abc.ABC):
    """
    Abstract base class for a Discord chatbot.
    """

    _num_last_messages: int = 20

    def _is_mentioned(self, message: discord_message.Message) -> bool:
        """
        Check if the bot is mentioned in the message.
        """
        return re.search(rf"<@&?{self.user.id}>", message.content) is not None

    def _remove_mention(self, message: discord_message.Message) -> str:
        """
        Remove the bot mention from the message content.
        """
        return re.sub(rf"<@&?{self.user.id}>", "", message.content).strip()

    def _format_message_to_openai_message(self, message: discord_message.Message) -> str:
        """
        Format a Discord message to OpenAI message format.
        """
        return message.content

    async def _build_message_history(self, message: discord_message.Message) -> list[str]:
        """
        Build the message history for the bot.
        """

        channel = message.channel

        if isinstance(channel, discord_threads.Thread):
            message_history = [self._format_message_to_openai_message(message) async for message in channel.history()]
            parent_message = await channel.parent.fetch_message(channel.id)
            message_history.append(self._format_message_to_openai_message(parent_message))

        elif isinstance(channel, discord_channel.TextChannel):
            message_history = [
                self._format_message_to_openai_message(message)
                async for message in channel.history(limit=self._num_last_messages)
            ]

        else:
            raise ValueError("Unsupported channel type")

        return message_history[::-1]
