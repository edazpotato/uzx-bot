import discord
from discord.ext import commands
from bot.custom import embeds
import json
from pathlib import Path


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xFF4500

    # ping command
    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.message.add_reaction("🏓")
        data = {
            "title": "🏓 Pong!",
            "color": self.color,
            "fields": [
                {
                    "title": "⏱ Latency",
                    "content": str(round(self.bot.latency, 3)) + "ms"
                }
            ]
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    @commands.command(name="prefix")
    async def prefix_command(self, ctx):
        await ctx.message.add_reaction("👌")
        p = Path(__file__).parents[1]
        p = Path(str(p) + "\\data\\guild_data\\prefixes.json")
        f = open(file=p, mode="r+")
        guilds = json.load(f)
        guildData = next((item for item in guilds if item["id"] == ctx.guild.id), None)
        if guildData is None:
            guildData = {"id": ctx.guild.id, "prefix": "$"}
            print(guilds)
            guilds.append(guildData.copy())
            guildsRawData = json.dumps(guilds)
            print(guildsRawData)
            f.write(guildsRawData)
        f.close()
        prefix = guildData["prefix"]
        data = {
            "title": "Prefix: `{0}`".format(prefix),
            "color": self.color
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)
