import discord
import asyncio

class DiscordBot(discord.Client):
    """
    A discord bot.

    Args:
        intents (discord.Intents): The intents for the bot.
    """

    def __init__(self, intents, hugchat_credentials=None):
        """
        Initializes the bot.

        Args:
            intents (discord.Intents): The intents for the bot.
        """
        super().__init__(intents=intents)
        self.commands = {
            "+help": self.handle_help,
        }

    async def on_ready(self):
        """
        Called when the bot has successfully connected to the Discord server.
        """
        print("Logged in as", self.user.name)

    async def on_message(self, message):
        """
        Decides what to do when a message is received.

        Args:
            message (discord.Message): The message received.
        """
        if message.author == self.user:
            return

        for command, function in self.commands.items():
            if message.content.startswith(command):
                await function(message)
                return

        if message.content.startswith("+"):
            await message.channel.send(
                "Was that meant to be a command? Because if that's the case, maaaan I have no idea what you are waiting for me to do :/"
            )
        return

    async def handle_help(self, message):
        """
        Handle the help command.

        Args:
            message (discord.Message): The message received.
        """
        await message.channel.send(
            "Commands:\n"
            "+help: Shows this message\n"
        )
