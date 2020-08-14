import json
from pathlib import Path
import aiohttp
import os
import typing
import random
import discord
from discord.ext import commands
from bot.custom import embeds, slow


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xFF69B4
        self.waiter = slow.Waiter()

    async def fetch(self, url, message, headers: typing.Optional[dict] = {}):
        await self.waiter.start(message)
        session = aiohttp.ClientSession()
        response = await session.get(url, headers=headers)
        res = await response.json()
        await session.close()
        await self.waiter.stop(message)
        return res

    # hello command
    @commands.command(name="hello", aliases=["hi"], hidden=True)
    async def hello_command(self, ctx):
        await ctx.message.add_reaction("👋")
        await ctx.send("Hi.")

    # is the earth flat?
    @commands.command(name="is", hidden=True)
    async def is_the_earth_flat_command(self, ctx, *, the_earth_flat: str):
        if the_earth_flat == "the earth flat?" or "the earth flat":
            await ctx.message.add_reaction(self.bot.get_emoji(713222235246035024))
            await ctx.send("NO")

    # pong command
    @commands.command(name="pong", hidden=True)
    async def pong_command(self, ctx):
        await ctx.message.add_reaction("🏓")
        data = {
            "title": "!gniP 🏓",
            "color": 0x0054FF,
            "fields": [
                {
                    "title": "ycnetaL ⏱",
                    "content": "`ms" + str(round(self.bot.latency*10000*-1), 0) + "`"
                }
            ]
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    # memes
    @commands.command(name="meme", aliases=["memes"])
    async def meme_command(self, ctx):
        res = await fetch("https://api.ksoft.si/images/random-meme", ctx.message, {"Authorization": "Bearer " + os.getenv("KSOFT_SI_TOKEN")})
        data = {
            "title": res["title"],
            "color": self.color,
            "image_url": res["image_url"],
            "description": "👍 {0}  👎 {1}\nFrom [{2}]({3})".format(res["upvotes"], res["downvotes"],
                                                                    res["subreddit"], res["source"])
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    # jokes
    @commands.command(name="joke", aliases=["jokes", "pun", "puns", "dadjoke", "dadjokes"])
    async def joke_command(self, ctx):
        await self.waiter.start(message)
        p = Path(__file__).parents[1]
        p = Path(str(p) + "\\data\\command_data\\jokes.json")
        f = open(file=p, mode="r")
        jsonData = json.load(f)
        f.close()
        await self.waiter.stop(message)
        jokes = jsonData["jokes"]
        jokeId = random.randint(0, len(jokes))
        joke = jokes[jokeId]
        data = {
            "description": joke,
            "color": self.color
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    # affermations
    @commands.command(name="affirmation", aliases=["affirm", "af"])
    async def affimation_command(self, ctx):
        await self.waiter.start(message)
        affirmation = await fetch("https://www.affirmations.dev/")
        await self.waiter.stop(message)
        data = {
            "color": self.color,
            "title": affirmation["affirmation"]
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    # clap!
    @commands.command(name="clap")
    async def clap_command(self, ctx):
        await ctx.message.delete()
        "👋"
    
    


