import json
import aiohttp
import os
import discord
from discord.ext import commands
from bot.custom import embeds, slow


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x00AA00
        self.hyApiKey = os.getenv("HYPIXEL_API_KEY")
        self.waiter = slow.Waiter()

    async def fetch(self, url, message):
        await self.waiter.start(message)
        session = aiohttp.ClientSession()
        response = await session.get(url)
        res = await response.json()
        await session.close()
        await self.waiter.stop(message)
        return res

    # general player data
    # TODO: add hypixel level
    @commands.command(name="player", aliases=["minecraft", "mc"])
    async def minecraft_player_command(self, ctx, username: str):
        uuidres = await self.fetch("https://api.mojang.com/users/profiles/minecraft/{0}".format(username), ctx.message)
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

    # player skin
    @commands.command(name="skin")
    async def minecraft_skin_command(self, ctx, username: str):
        uuidres = await self.fetch(f"https://api.mojang.com/users/profiles/minecraft/{username}", ctx.message)
        uuid = uuidres["id"]
        playername = uuidres["name"]
        data = {
            "title": "**__{0}__**".format(playername),
            "color": self.color,
            "image_url": "https://crafatar.com/renders/body/{0}.png".format(uuid)
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)



