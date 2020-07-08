import discord
from discord.ext import commands
import os
#from dotenv import load_dotenv
from bot.custom import cogs


# Load environment variables
#load_dotenv()


async def stop(bot):
    print("Logging out of discord...")
    await bot.logout()


def run():
    def prefix(bot, message):
        customprefix = "$"
        prefixes = [
            "{0} ".format(customprefix),
            "{0}".format(customprefix),
            "{0} ".format(bot.user.name),
            "{0}".format(bot.user.name),
            "<@!{0}> ".format(bot.user.id),
            "<@!{0}>".format(bot.user.id),
            "<@{0}> ".format(bot.user.id),
            "<@{0}>".format(bot.user.id),
            "{0} ".format(message.guild.me.nick),
            "{0}".format(message.guild.me.nick)
        ]

        return prefixes

    # create bot
    description = "The last discord bot you'll ever need!"
    client = commands.Bot(
        command_prefix=prefix,
        case_insensitive=True,
        description=description,
        owner_id=int(os.getenv("OWNER_ID"))
    )

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
        activity = discord.Activity(type=discord.ActivityType.watching, name=" for @{0.user.name} help".format(client))
        await client.change_presence(activity=activity)

    # register cogs
    cogloader = cogs.CogLoader(client)
    cogloader.loadcogs()

    client.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    run()
