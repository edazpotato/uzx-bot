import os
import typing
import discord
from discord.ext import commands
from bot.custom import embeds


class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x03FCDB

    @commands.group(aliases=["a"])
    @commands.is_owner()
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            user = self.bot.get_user(int(self.bot.owner_id))
            data = {
                "title": "Hello *{0}*".format(user),
                "color": self.color
            }
            embed = embeds.RichEmbed(self.bot, data)
            await embed.send(ctx)

    @admin.command()
    async def raw(self, ctx, amount: typing.Optional[int] = 1):
        messages = await ctx.channel.history(limit=amount+1).flatten()
        message = messages[amount]
        message.content = message.content.replace("`", "\\`")
        data = {
            "color": self.color,
            "author": {
                "name": "{0}#{1}".format(message.author.name, message.author.discriminator),
                "icon_url": message.author.avatar_url
            },
            "description": "Raw message content:```\n{0}\n```".format(message.content)
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)