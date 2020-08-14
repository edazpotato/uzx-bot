import discord

class Waiter:
    def __init__(self):
        pass

    async def start(self, message):
        await message.add_reaction("<a:loading:732421120954990618>")

    async def stop(self, message):
        await message.remove_reaction("<a:loading:732421120954990618>", message.guild.me)