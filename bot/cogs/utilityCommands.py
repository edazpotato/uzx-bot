import discord
from discord.ext import commands
from bot.custom import embeds


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
