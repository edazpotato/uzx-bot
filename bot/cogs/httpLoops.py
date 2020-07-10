from discord.ext import tasks, commands
import time
import aiohttp


# all looping things (like sending stats to dbl or statuspage)
class Loop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.looper.start()
        self.i = 0

    def cog_unload(self):
        self.looper.cancel()

    @tasks.loop(minutes=1)
    async def looper(self):
        print("Looped: " + str(self.i));
        self.i += 1
        await self.statuspage()

    @looper.before_loop
    async def before_looper(self):
        print('waiting for bot to start before sending http things...')
        await self.bot.wait_until_ready()

    # things to loop
    async def statuspage(self):
        api_key = '52a21606-f85b-49b6-a1bb-44ee2948b878'
        page_id = 'yly9drz8dt5f'
        metric_id = 'n7w2zgrp830t'

        ts = print(int(time.time()))
        latency = print(self.bot.latency)

        url = "https://api.statuspage.io/v1/pages/" + page_id + "/metrics/data"
        headers = {"Authorization": "OAuth " + api_key}
        payload = {"data": {metric_id: {"timestamp": ts, "value": latency}}}
        session = aiohttp.ClientSession()
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as resp:
                print(resp.status)
                print(await resp.text())
            session.close()
