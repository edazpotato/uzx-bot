import os

# Load environment variables if not on heroku
if not os.getenv("DISCORD_TOKEN"):
    from dotenv import load_dotenv
    load_dotenv()

import discord
import logging
from bot import bot


# setup Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


lifeIsGood = True
if lifeIsGood:
    print("Life is good bois")
    print("Attempting to start the bot...")
    bot.run()

