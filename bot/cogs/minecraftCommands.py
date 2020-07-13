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

    # memes
    @commands.command(name="player", aliases=["minecraft", "mc"])
    async def minecraft_player_command(self, ctx, username: str):
        await ctx.message.add_reaction("👌")

        uuidRes = await fetch("https://api.mojang.com/users/profiles/minecraft/{0}".format(username))
        uuid = uuidRes["id"]
        playerName = uuidRes["name"]
        nameHitory = await fetch("https://api.mojang.com/user/profiles/{0}/names".format(uuid))
        print(nameHitory)
        data = {
            "title": "{0}".format(playerName),
            "color": self.color,
            "thumbnail_url": "https://crafatar.com/avatars/{0}".format(uuid),
            "image_url": "https://crafatar.com/renders/body/{0}.png".format(uuid),
            "description": "*UUID*: `{0}`".format(uuid),
            "fields": [
                {
                    "title": "Username",
                    "content": playerName,
                    "inline": True
                },
                {
                    "title": "UUID",
                    "content": uuid,
                    "inline": True
                },
            ]
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

