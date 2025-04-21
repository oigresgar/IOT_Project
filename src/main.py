import os

from discord import Intents
from dotenv import load_dotenv

from Bot.DiscordBot import DiscordBot

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    intents = Intents.default()
    intents.message_content = True
    bot = DiscordBot(intents)
    bot.run(token)
