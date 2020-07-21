from discord.ext import tasks, commands
import time
import math
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

        ts = int(time.time())
        latency = math.floor(self.bot.latency*100)

        url = f"https://api.statuspage.io/v1/pages/{page_id}/metrics/{metric_id}/data.json"
        headers = {"Authorization": "OAuth " + api_key}
        payload = {"data": {"timestamp": ts, "value": latency}}
        session = aiohttp.ClientSession()
        response = await session.post(url, headers=headers, data=payload)
        print(response.status)
        print(await response.text())
        await session.close()
