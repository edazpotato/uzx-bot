import os
#import pymongo
import discord
from discord.ext import commands
from bot.custom import cogs



async def stop(bot):
    print("Logging out of discord...")
    await bot.logout()


def run():
    #dbPass = "9RyOgLLCvIPvFs5c"
    #dbClient = pymongo.MongoClient(f"mongodb+srv://test_user_1:{dbPass}@uzxdb.xswzv.gcp.mongodb.net/uzxdb?retryWrites=true&w=majority")
    #db = dbClient.test
    #for database_name in client.list_database_names():
    #    print("Database - " + database_name)
    #    for collection_name in client.get_database(database_name).list_collection_names():
    #        print(collection_name)

    def prefix(bot, message):
        guild = message.guild.id
        id = bot.user.id
        customprefix = "uzx"
        
        prefixes = [
            f"{customprefix} ",
            f"{customprefix}",
            f"<@!{id}> ",
            f"<@!{id}>",
            f"<@{id}> ",
            f"<@{id}>"
        ]

        return prefixes

    # create bot
    description = "The last discord bot you'll ever need!"
    client = commands.Bot(
        command_prefix=prefix,
        help_command=None,
        case_insensitive=True,
        description=description,
        owner_id=int(os.getenv("OWNER_ID"))
    )

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
        activity = discord.Activity(type=discord.ActivityType.watching, name=" for @{0.user.name} help | Now in Beta! - edaz.codes/uzx".format(client))
        await client.change_presence(activity=activity)

    # register cogs
    cogloader = cogs.CogLoader(client)
    cogloader.loadcogs()

    client.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    run()
