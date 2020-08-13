import discord
from discord.ext import commands
from bot.custom import embeds
import json
import typing
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
                    "content": "`" + str(round(self.bot.latency*10000), 0) + "ms`"
                }
            ]
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    #@commands.command(name="prefix")
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

    @commands.command(name="invite", aliases=["inv", "add"])
    async def invite_bot_command(self, ctx):
        # url = f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot"
        # await ctx.send("Add me to your server using this URL: *{0}*".format(url))
        await ctx.send("I'm currently in a private beta. You can apply to have me added to your server at https://edaz.codes/uzx/")
        await ctx.send(f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=2146958847")

    @commands.command(name="emoji", aliases=["se", "steal", "stealemoji"])
    async def emoji_steal_command(self, ctx, emoji: typing.Optional[discord.Emoji]):
        if emoji is None:
            data = {
                "color": self.color,
                "title": "Theivery error:",
                "description": "For now you can't steal animated emoji if you don't have nitro :(\n> If you want to use a bult-in Discord emoji somewhere other than Discord, do `:emojiName:` but put a `\` before it like this: `\:emojiName:`. Then you can copy and paste it like a normal text character"
            }
        else:
            data = {
                "color": self.color,
                "title": f":{emoji.name}:",
                "description": "Click to the image, click *open original*  to open it in your browser, then right click and choose *save image as*",
                "image_url": emoji.url
            }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    @commands.command(name="info", aliases=["about"])
    async def info_command(self, ctx):
        owner = self.bot.get_user(self.bot.owner_id)
        data = {
            "title": "Bot info",
            "color": self.color,
            "description": f"```Owner: {owner.name}#{owner.discriminator}\nLanguage: Python 3\nLibrary: Discord.py```"
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    @commands.command(name="help", aliases=["command", "commands"])
    async def help_command(self, ctx):
        data = {
            "color": self.color,
            "title": "Need help? We've got you covered",
            "description": "[Commands](https://edazpotato.github.io/uzx/docs/#/ref/commands/)\n[Docs](https://edazpotato.github.io/uzx/docs/)   (please help us write these)\n[Support server](https://discord.gg/mzR7eeZ)"
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)
