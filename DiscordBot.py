import io
import os
import discord
import json
from dotenv import load_dotenv
from AmiLab import AmiLabHttp as AmiLab


class DiscordBot(discord.Client):
    """
    A discord bot.

    Args:
        intents (discord.Intents): The intents for the bot.
    """

    def __init__(self, intents):
        """
        Initializes the bot.

        Args:
            intents (discord.Intents): The intents for the bot.
        """
        super().__init__(intents=intents)
        self.ami_lab = AmiLab(
            url=os.getenv("AMI_LAB_URL"),
            token=os.getenv("AMI_LAB_TOKEN"),
        )
        self.commands = {
            "+help": self.handle_help,
            "+snapshot": self.handle_snapshot,
            "+get_state": self.handle_get_state,
            "+post_service": self.handle_post_service,
        }

    async def on_ready(self):
        """
        Called when the bot has successfully connected to the Discord server.
        """
        print("Logged in as", self.user.name)

    async def on_message(self, message: discord.Message):
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

    async def handle_help(self, message: discord.Message):
        """
        Handle the help command.

        Args:
            message (discord.Message): The message received.
        """
        await message.channel.send(
            "Commands:\n"
            "   +help: Shows this message\n"
            "   +snapshot: Sends a snapshot from the AmiLab camera\n"
            "   +get_state <entity_id>: Gets the state of the specified entity\n"
            "   +post_service <entity_id> <service> <command> [extra_data]: Posts a service command to the specified entity\n"
        )

    async def handle_snapshot(self, message: discord.Message):
        img = self.ami_lab.get_snapshot()
        img = io.BytesIO(img)
        await message.channel.send(file=discord.File(img, "snapshot.jpg"))
        return

    async def handle_get_state(self, message: discord.Message):
        """
        Handle the get_state command.

        Args:
            message (discord.Message): The message received.
        """
        try:
            entity_id = message.content.split()[1]
            state = self.ami_lab.get_state(entity_id)
            await message.channel.send(f"State of {entity_id}: {state}")
        except IndexError:
            await message.channel.send("Usage: +get_state <entity_id>")
        except Exception as e:
            await message.channel.send(f"Error: {e}")

    async def handle_post_service(self, message: discord.Message):
        """
        Handle the post_service command.

        Args:
            message (discord.Message): The message received.
        """
        try:
            parts = message.content.split()
            entity_id = parts[1]
            service = parts[2]
            command = parts[3]
            extra_data = {}
            if len(parts) > 4:
                extra_data_msg = " ".join(parts[4:])
                try:
                    extra_data = json.loads(extra_data_msg)
                except json.JSONDecodeError:
                    await message.channel.send(
                        "Error: extra_data must be a valid JSON object"
                    )
                    return
            response = self.ami_lab.post_service(
                entity_id, service, command, extra_data
            )
            response = json.dumps(response, indent=4)
            await message.channel.send(f"Service response: {response}")
        except IndexError:
            await message.channel.send(
                "Usage: +post_service <entity_id> <service> <command> [extra_data]"
            )
        except Exception as e:
            await message.channel.send(f"Error: {e}")


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    bot = DiscordBot(intents)
    bot.run(token)
