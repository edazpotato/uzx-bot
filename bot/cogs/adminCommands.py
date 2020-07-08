import os
import discord
from discord.ext import commands
from bot.custom import embeds


class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x00FF00

    @commands.group()
    @commands.is_owner()
    async def admin(self, ctx):
        user = self.bot.get_user(int(self.bot.owner_id))
        data = {
            "title": "Hello {0}".format(user),
            "color": self.color
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)
