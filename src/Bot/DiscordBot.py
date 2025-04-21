import io
import json
import os
from time import sleep

import discord
from PIL import Image

from AmiLab.AmiLab import AmiLabHttp as AmiLab
from Model.YoloModel import YoloModel


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
        self.yolo_model = YoloModel()
        self.commands = {
            "+help": self.handle_help,
            "+snapshot": self.handle_snapshot,
            "+get_state": self.handle_get_state,
            "+post_service": self.handle_post_service,
            "+count_people": self.handle_count_people,
            "+request_access_to": self.handle_access_request,
            "+mock": self.handle_mock,
        }
        self.mock = False

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
            "   +count_people: Counts the number of people in the AmiLab camera image\n"
            "   +request_access_to <num_people>: Requests access to the specified number of people\n"
            "   +mock: Toggles mock mode (for testing purposes)\n"
        )

    async def handle_snapshot(self, message: discord.Message):
        img = self.ami_lab.get_snapshot(mock=self.mock)
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

    async def handle_count_people(self, message: discord.Message):
        """
        Handle the count_people command.

        Args:
            message (discord.Message): The message received.
        """
        try:
            count, plot_img = self.capture_and_count_people()
            with io.BytesIO() as sent_img:
                plot_img.save(fp=sent_img, format="JPEG")
                await message.channel.send(f"Number of people detected: {count}")
                sent_img.seek(0)
                await message.channel.send(file=discord.File(sent_img, "plot.jpeg"))
        except Exception as e:
            await message.channel.send(f"Error: {e}")

    def capture_and_count_people(self):
        img_bytes = self.ami_lab.get_snapshot(mock=self.mock)
        with io.BytesIO(img_bytes) as img_bytes:
            img = Image.open(img_bytes)
            count, plot_img = self.yolo_model.count_people_in_img(img)
        return count, plot_img

    async def handle_access_request(self, message: discord.Message):
        # Try to obtain num of people rqquested
        try:
            parts = message.content.split()
            num_people = int(parts[1])
        except ValueError:
            await message.channel.send("Usage: +request_access_to <num_people>")
            return
        except IndexError:
            await message.channel.send("Usage: +request_access_to <num_people>")
            return
        print(f"Requested number of people: {num_people}")

        # Get the number of people in the image
        try:
            count, plot_img = self.capture_and_count_people()
        except Exception as e:
            await message.channel.send(f"Error: {e}")
            return
        # Until the number of people is equal to the requested number
        # set the light to red
        print(f"Number of people detected: {count}")

        counter = 0
        try:
            while count < num_people:
                if counter > 10:
                    await message.channel.send(
                        "Access denied. Too many attempts. Please try again later."
                    )
                    return
                counter += 1
                sleep(2)
                # Get the number of people in the image
                count, plot_img = self.capture_and_count_people()
                print(f"Number of people detected: {count}")
                if count < num_people:
                    # Set the light to red
                    self.ami_lab.post_service(
                        entity_id="light.lampara_derecha",
                        service="light",
                        command="turn_on",
                        extra_data={"brightness_pct": "100", "rgb_color": [255, 0, 0]},
                    )
                    print("Color set to red")
                    # Send the image with the number of people detected
                    with io.BytesIO() as sent_img:
                        plot_img.save(fp=sent_img, format="JPEG")
                        sent_img.seek(0)

                        await message.channel.send(
                            f"Number of people detected: {count}. Access denied >:(. Retrying analysis..."
                        )
                        await message.channel.send(
                            file=discord.File(sent_img, "plot.jpeg")
                        )
            # Set the light to green
            self.ami_lab.post_service(
                entity_id="light.lampara_derecha",
                service="light",
                command="turn_on",
                extra_data={"brightness_pct": "100", "rgb_color": [0, 255, 0]},
            )
            # Send the image with the number of people detected
            with io.BytesIO() as sent_img:
                plot_img.save(fp=sent_img, format="JPEG")
                sent_img.seek(0)
                await message.channel.send(
                    f"Number of people detected: {count}. Access granted ^_^."
                )
                sent_img.seek(0)
                await message.channel.send(file=discord.File(sent_img, "plot.jpeg"))
        except Exception as e:
            await message.channel.send(f"Error: {e}")
        return

    async def handle_mock(self, message: discord.Message):
        """
        Handle the mock command.

        Args:
            message (discord.Message): The message received.
        """
        self.mock = not self.mock
        if self.mock:
            await message.channel.send("Mock mode enabled.")
        else:
            await message.channel.send("Mock mode disabled.")
