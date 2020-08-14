import discord
from discord.ext import commands
import asyncio
import youtube_dl
from bot.custom import embeds, slow

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.waiter = slow.Waiter()

    @commands.command(name="join")
    async def join_command(self, ctx):
        """Joins a voice channel"""
        if ctx.author.voice.channel is not None:
            channel = ctx.author.voice.channel
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)
            await channel.connect()
        else:
            msg = await ctx.send("You ain't in a voice channel mate")
            await asyncio.sleep(2)
            await msg.delete()

    @commands.command(name="play", aliases=["yt", "p"])
    async def play_command(self, ctx, *, url):
        """Streams from a url (doesn't predownload)"""

        await self.waiter.start(ctx.message)
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f"Player error: {e}") if e else None)
        await self.waiter.stop(ctx.message)
        data = {
            "title": "Now playing: ",
            "description": player.title,
            "color": ctx.author.color
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    @commands.is_owner()
    @commands.command(name="volume", aliases=["vol", "v"])
    async def volume_command(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            msg = await ctx.send("Not connected to a voice channel.")
            await asyncio.sleep(2)
            await msg.delete()
        else:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"Changed volume to {volume}%")

    @commands.command(name="disconnect", aliases=["dc", "stop"])
    async def disconnect_command(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play_command.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                msg = await ctx.send("You are not connected to a voice channel.")
                await asyncio.sleep(2)
                await msg.delete()
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()