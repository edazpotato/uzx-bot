import os
import discord
import logging
from bot import bot
import sentry_sdk

# start sentry
sentry_sdk.init("https://1f1629f5fcec49d293bd9af58a917b06@o414617.ingest.sentry.io/5305306")

# Load environment variables if not on heroku
if not os.getenv("DISCORD_TOKEN"):
    from dotenv import load_dotenv
    load_dotenv()


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

