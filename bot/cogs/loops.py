from discord.ext import tasks, commands


# all looping things (like sending stats to dbl or statuspage)
class Loop(commands.cog):

    def __init__(self, bot):
        self.bot = bot
        self.dblKey = "";

    async def start(self):
        pass