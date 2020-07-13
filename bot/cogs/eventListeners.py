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
            data = {
                "color": self.color,
                "title": "ERROR: `{0}`",
                "description": "You need the following permission(s) in order to do that:",
                "fields": [
                    {
                        "description": "```{0}```".format(error.missing_perms())
                    }
                ]
            }
            embed = embeds.RichEmbed(self.bot, data)
            return await embed.send(ctx)
        if isinstance(error, commands.BotMissingPermissions):
            data = {
                "color": self.color,
                "title": "ERROR: `{0}`",
                "description": "I need the following permission(s) in order to do that:",
                "fields": [
                    {
                        "description": "```{0}```".format(error.missing_perms())
                    }
                ]
            }
            embed = embeds.RichEmbed(self.bot, data)
            return await embed.send(ctx)
        print(str(error))
        raise error
