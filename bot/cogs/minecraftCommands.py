import json
import aiohttp
import os
import discord
from discord.ext import commands
from bot.custom import embeds


async def fetch(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    res = await response.json()
    await session.close()
    return res



class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x00AA00

    # general player data
    # TODO: add hypixel level
    @commands.command(name="player", aliases=["minecraft", "mc"])
    async def minecraft_player_command(self, ctx, username: str):
        await ctx.message.add_reaction("<a:loading:732421120954990618>")
        uuidres = await fetch("https://api.mojang.com/users/profiles/minecraft/{0}".format(username))
        uuid = uuidres["id"]
        playername = uuidres["name"]
        data = {
            "title": "**__{0}__**".format(playername),
            "color": self.color,
            "thumbnail_url": "https://crafatar.com/avatars/{0}.png".format(uuid),
            "description": "*UUID*: `{0}`".format(uuid)
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)
        await ctx.message.remove_reaction("<a:loading:732421120954990618>", ctx.me)

    # player skin
    @commands.command(name="skin", aliases=["s"])
    async def minecraft_skin_command(self, ctx, username: str):
        await ctx.message.add_reaction("<a:loading:732421120954990618>")

        uuidres = await fetch("https://api.mojang.com/users/profiles/minecraft/{0}".format(username))
        uuid = uuidres["id"]
        playername = uuidres["name"]
        data = {
            "title": "**__{0}__**".format(playername),
            "color": self.color,
            "image_url": "https://crafatar.com/renders/body/{0}.png".format(uuid)
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)
        await ctx.message.remove_reaction("<a:loading:732421120954990618>", ctx.me)



