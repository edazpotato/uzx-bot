import discord
from discord.ext import commands
from bot.custom import embeds


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xadd8e6

    # error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing the reqired permission(s) to do that.")
            return await ctx.send("Ask your guild admin for the followwing permission(s) in order to be able to use this command: \n`{0}`".format(error.missing_perms))
        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send("I need the `{0}` permission(s) to do that!".format(error.missing_perms))
        print(str(error))
        raise error
