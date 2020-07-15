import os
import ast
import json
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

    @admin.command(name="raw", aliases=["r"])
    async def raw_subcommand(self, ctx, amount: typing.Optional[int] = 1):
        messages = await ctx.channel.history(limit=amount+1).flatten()
        message = messages[amount]
        msgcontent = discord.utils.escape_mentions(discord.utils.escape_markdown(message.content))
        data = {
            "color": self.color,
            "author": {
                "name": "{0}#{1}".format(message.author.name, message.author.discriminator),
                "icon_url": message.author.avatar_url
            },
            "description": "Raw message content:```\n\n{0}\n\n```".format(msgcontent)
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    @admin.command(name="embed", aliases=["e"])
    async def embed_subcommand(self, ctx, *, data: typing.Optional[str]):
        json_acceptable_string = data.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        if d is None:
            d = {
                "title": "ERROR: no embed code provided",
                "color": self.color
            }
        else:
            d = ast.literal_eval(data)
        embed = embeds.RichEmbed(self.bot, d)
        await embed.send(ctx)