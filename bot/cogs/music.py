################################################################
# Code completely based off https://github.com/Jess-v/music-bot #
################################################################

import asyncio
import os

import discord
import youtube_dl
from discord.ext import commands
from pathlib import Path
from bot.custom import embeds, slow

# make youtube_dl shut up
youtube_dl.utils.bug_reports_message = lambda: ''


class Queue(list):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_song = None
        self._skip_voters = []

    def next_song(self):
        self._current_song = self.pop(0)

        return self._current_song

    def clear(self):
        super().clear()
        self._current_song = None

    def add_skip_vote(self, voter: discord.Member):
        self._skip_voters.append(voter)

    def clear_skip_votes(self):
        self._skip_voters.clear()

    @property
    def skip_voters(self):
        return self._skip_voters

    @property
    def current_song(self):
        return self._current_song

    def get_embed(self, song_id: int):
        if song_id <= 0:
            song = self.current_song
        else:
            song = self[song_id-1]

        if len(song.description) > 300:
            song['description'] = f'{song.description[:300]}...'

        embed = discord.Embed(title="Audio Info")
        embed.set_thumbnail(url=song.thumbnail)
        embed.add_field(name='Song', value=song.title, inline=True)
        embed.add_field(name='Uploader', value=song.uploader, inline=True)
        embed.add_field(name='Duration', value=song.duration_formatted, inline=True)
        embed.add_field(name='Description', value=song.description, inline=True)
        embed.add_field(name='Upload Date', value=song.upload_date_formatted, inline=True)
        embed.add_field(name='Views', value=song.views, inline=True)
        embed.add_field(name='Likes', value=song.likes, inline=True)
        embed.add_field(name='Dislikes', value=song.dislikes, inline=True)
        embed.add_field(name='Requested By', value=song.requested_by_username, inline=True)

        return embed


class Song(dict):

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    def __init__(self, url: str, author: discord.Member):
        super().__init__()
        self.download_info(url, author)

    @property
    def url(self):
        return self.get('url', None)

    @property
    def title(self):
        return self.get('title', 'Unable To Fetch')

    @property
    def uploader(self):
        return self.get('uploader', 'Unable To Fetch')

    @property
    def duration_raw(self):
        return self.get('duration', 0)

    @property
    def duration_formatted(self):
        minutes, seconds = self.duration_raw // 60, self.duration_raw % 60
        return f'{minutes}m, {seconds}s'

    @property
    def description(self):
        return self.get('description', 'Unable To Fetch')

    @property
    def upload_date_raw(self):
        return self.get('upload_date', '01011970')

    @property
    def upload_date_formatted(self):
        m, d, y = self.upload_date_raw[4:6], self.upload_date_raw[6:8], self.upload_date_raw[0:4]
        return f'{m}/{d}/{y}'

    @property
    def views(self):
        return self.get('view_count', 0)

    @property
    def likes(self):
        return self.get('like_count', 0)

    @property
    def dislikes(self):
        return self.get('dislike_count', 0)

    @property
    def thumbnail(self):
        return self.get('thumbnail', 'http://i.imgur.com/dDTCO6e.png')

    @property
    def requested_by_username(self):
        return self.get('requested_by', 'Unknown requester')

    @property
    def requested_by_id(self):
        return self.get('requested_by_id', 1)

    def download_info(self, url: str, author: discord.Member):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            self.update(ydl.extract_info(url, download=False))

            if not url.startswith('https'):
                self.update(ydl.extract_info(self['entries'][0]['webpage_url'], download=False))

            self['url'] = url
            self['requested_by'] = str(author.name)
            self['requested_by_id'] = author.id

# 20 minutes, in seconds
DURATION_CEILING = 20 * 60

DURATION_CEILING_STRING = '20mins'

SONGS_PER_PAGE = 10


def set_str_len(s: str, length: int):
    '''Adds whitespace or trims string to enforce a specific size'''

    return s.ljust(length)[:length]


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.music_queues = {}
        self.voice_clients = {}
        self.waiter = slow.Waiter()

    @commands.command()
    async def play(self, ctx: commands.Context, url: str, *args: str):
        '''Adds a song to the queue either by YouTube URL or YouTube Search.'''

        music_queue = self.music_queues.get(ctx.guild, None)
        voice = self.voice_clients.get(ctx.guild)

        if music_queue is None:
            music_queue = Queue()
            self.music_queues[ctx.guild] = music_queue

        try:
            channel = ctx.message.author.voice.channel
        except:
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You're not connected to a voice channel.", delete_after=2)
            return

        if voice is not None and not self.client_in_same_channel(ctx.message.author, ctx.guild):
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You're not in my voice channel.", delete_after=2)
            return

        if not url.startswith('https://'):
            url = f'ytsearch1:{url} {" ".join(args)}'

        song = Song(url, ctx.author)
        valid_song, song_err = self.song_error_check(song)

        if not valid_song:
            await ctx.send(song_err)
            return

        if voice is None or not voice.is_connected():
            self.voice_clients[ctx.guild] = await channel.connect()

        music_queue.append(song)
        await ctx.send(f'Queued song: {song.title}')

        await self.play_all_songs(ctx.guild)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def stop(self, ctx: commands.Context):
        '''Admin command that stops playback of music and clears out the music queue.'''

        voice = self.voice_clients.get(ctx.guild)
        queue = self.music_queues.get(ctx.guild)

        if self.client_in_same_channel(ctx.message.author, ctx.guild):
            voice.stop()
            queue.clear()
            self.voice_clients[ctx.guild] = None
            await ctx.message.add_reaction("👋")
            await ctx.send("Thanks for listening!", delete_after=2)
            await voice.disconnect()
        else:
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You're not in a voice channel with me.", delete_after=2)

    @commands.command()
    async def skip(self, ctx: commands.Context):
        '''Puts in your vote to skip the currently played song.'''

        voice = self.voice_clients.get(ctx.guild)
        queue = self.music_queues.get(ctx.guild)

        if not self.client_in_same_channel(ctx.message.author, ctx.guild):
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You're not in a voice channel with me.", delete_after=2)
            return

        if voice is None or not voice.is_playing():
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("I'm not playing a song right now.", delete_after=2)
            return

        if ctx.author in queue.skip_voters:
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You've already voted to skip this song.", delete_after=2)
            return

        channel = ctx.message.author.voice.channel
        required_votes = round(len(channel.members) / 2)

        queue.add_skip_vote(ctx.author)

        if len(queue.skip_voters) >= required_votes:
            await ctx.send("Skipping song after successful vote.", delete_after=2)
            voice.stop()
        else:
            await ctx.message.add_reaction("🗳️")
            await ctx.send(f"You voted to skip this song. {required_votes - len(queue.skip_voters)} more votes are required.", delete_after=2)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def fskip(self, ctx: commands.Context):
        '''Admin command that forces skipping of the currently playing song.'''

        voice = self.voice_clients.get(ctx.guild)

        if not self.client_in_same_channel(ctx.message.author, ctx.guild):
            await ctx.send("You're not in a voice channel with me.", delete_after=2)
        elif voice is None or not voice.is_playing():
            await ctx.send("I'm not playing a song right now.")
        else:
            voice.stop()

    @commands.command()
    async def songinfo(self, ctx: commands.Context, song_index: int = 0):
        '''Print out more information on the song currently playing.'''

        queue = self.music_queues.get(ctx.guild)

        if song_index not in range(len(queue) + 1):
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("A song does not exist at that index in the queue.", delete_after=2)
            return

        embed = queue.get_embed(song_index)
        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx: commands.Context, song_id: int = None):
        '''Removes the last song you requested from the queue, or a specific song if queue position specified.'''

        if not self.client_in_same_channel(ctx.message.author, ctx.guild):
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You're not in a voice channel with me.", delete_after=2)
            return

        if song_id is None:
            queue = self.music_queues.get(ctx.guild)

            for index, song in reversed(list(enumerate(queue))):
                if ctx.author.id == song.requested_by_id:
                    queue.pop(index)
                    await ctx.send(f'Song "{song.title}" removed from queue.', delete_after=2)
                    return
        else:
            queue = self.music_queues.get(ctx.guild)

            try:
                song = queue[song_id - 1]
            except IndexError:
                await ctx.message.add_reaction("<:no:713222233627164673>")
                await ctx.send('An invalid index was provided.', delete_after=2)
                return

            if ctx.author.id == song.requested_by_id:
                queue.pop(song_id - 1)
                await ctx.send(f'Song {song.title} removed from queue.', delete_after=2)
            else:
                await ctx.message.add_reaction("<:no:713222233627164673>")
                await ctx.send('You cannot remove a song requested by someone else.', delete_after=2)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def fremove(self, ctx: commands.Context, song_id: int = None):
        '''Admin command to forcibly remove a song from the queue by it's position.'''

        queue = self.music_queues.get(ctx.guild)

        if not self.client_in_same_channel(ctx.message.author, ctx.guild):
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You're not in a voice channel with me.", delete_after=2)
            return

        if song_id is None or 0:
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You need to specify a song by it's queue index.", delete_after=2)
            return

        try:
            song = queue[song_id - 1]
        except IndexError:
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send('A song does not exist at this queue index.', delete_after=2)
            return

        queue.pop(song_id - 1)
        await ctx.send(f'Removed {song.title} from the queue.')
        return

    @commands.command()
    async def queue(self, ctx: commands.Context, page: int = 1):
        '''Prints out a specified page of the music queue, defaults to first page.'''

        queue = self.music_queues.get(ctx.guild)

        if not self.client_in_same_channel(ctx.message.author, ctx.guild):
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("You're not in a voice channel with me.", delete_after=2)
            return

        if not len(queue):
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("I don't have anything in my queue right now.", delete_after=2)
            return

        if len(queue) < SONGS_PER_PAGE * (page - 1):
            await ctx.message.add_reaction("<:no:713222233627164673>")
            await ctx.send("I don't have that many pages in my queue.", delete_after=2)
            return

        to_send = f'```\n    {set_str_len("Song", 66)}{set_str_len("Uploader", 36)}Requested By\n'

        for pos, song in enumerate(queue[:SONGS_PER_PAGE * page], start=SONGS_PER_PAGE * (page - 1)):
            title = set_str_len(song.title, 65)
            uploader = set_str_len(song.uploader, 35)
            requested_by = song.requested_by_username
            to_send += f'{set_str_len(f"{pos + 1})", 4)}{title}|{uploader}|{requested_by}\n'

        await ctx.send(to_send + '```')

    async def play_all_songs(self, guild: discord.Guild):
        queue = self.music_queues.get(guild)

        # Play next song until queue is empty
        while len(queue) > 0:
            await self.wait_for_end_of_song(guild)

            song = queue.next_song()

            await self.play_song(guild, song)

        # Disconnect after song queue is empty
        await self.inactivity_disconnect(guild)

    async def play_song(self, guild: discord.Guild, song: Song):
        '''Downloads and starts playing a YouTube video's audio.'''

        audio_dir = os.path.join('.', 'audio')
        audio_path = os.path.join(audio_dir, f'{guild.id}.mp3')
        voice = self.voice_clients.get(guild)

        queue = self.music_queues.get(guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': audio_path
        }

        Path(audio_dir).mkdir(parents=True, exist_ok=True)

        try:
            os.remove(audio_path)
        except OSError:
            pass

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([f'{song.url}'])
            except:
                await self.play_all_songs(guild)
                print('Error downloading song. Skipping.')
                return

        voice.play(discord.FFmpegPCMAudio(audio_path))
        queue.clear_skip_votes()

    async def wait_for_end_of_song(self, guild: discord.Guild):
        voice = self.voice_clients.get(guild)
        while voice.is_playing():
            await asyncio.sleep(1)

    async def inactivity_disconnect(self, guild: discord.Guild):
        '''If a song is not played for 5 minutes, automatically disconnects bot from server.'''

        voice = self.voice_clients.get(guild)
        queue = self.music_queues.get(guild)
        last_song = queue.current_song

        await asyncio.sleep(300)
        if queue.current_song == last_song:
            await voice.disconnect()

    def client_in_same_channel(self, author: discord.Member, guild: discord.Guild):
        '''Checks to see if a client is in the same channel as the bot.'''

        voice = self.voice_clients.get(guild)

        try:
            channel = author.voice.channel
        except AttributeError:
            return False

        return voice is not None and voice.is_connected() and channel == voice.channel

    @staticmethod
    def song_error_check(song: Song):
        ''' Checks song properties to ensure that the song is both valid and doesn't match any filtered properties'''

        if song.url is None:
            return False, 'Invalid URL provided or no video found.'

        if song.get('is_live', True):
            return False, 'Invalid video - either live stream or unsupported website.'

        if song.duration_raw > DURATION_CEILING:
            return False, f'Video is too long. Keep it under {DURATION_CEILING_STRING}.'

        return True, None
