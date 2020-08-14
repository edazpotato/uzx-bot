import discord
import datetime


class RichEmbed:
    def __init__(self, bot, data):
        if "title" not in data:
            data["title"] = ""
        if "color" not in data:
            data["color"] = 0x000000
        if "description" not in data:
            data["description"] = ""
        embed = discord.Embed(title=data["title"], description=data["description"], color=data["color"], timestamp=datetime.datetime.utcnow())
        if "thumbnail_url" in data:
            embed.set_thumbnail(url=data["thumbnail_url"])
        if "url" in data:
            embed.url = data["url"]
        if "image_url" in data:
            embed.set_image(url=data["image_url"])
        if "author" in data:
            if "name" not in data["author"]:
                data["author"]["name"] = ""
            if "url" not in data["author"]:
                data["author"]["url"] = ""
            if "icon_url" not in data["author"]:
                data["author"]["icon_url"] = ""
            embed.set_author(
                name=data["author"]["name"],
                url=data["author"]["url"],
                icon_url=data["author"]["icon_url"]
            )
        if "fields" in data:
            for field in data["fields"]:
                if "title" not in field:
                    field["title"] = "\u200b"
                if "content" not in field:
                    field["content"] = "\u200b"
                if "inline" not in field:
                    field["inline"] = False
                if "blank" in field:
                    if field["blank"]:
                        embed.add_field(name="\u200b", value="\u200b")
                else:
                    embed.add_field(name=field["title"], value=field["content"], inline=field["inline"])
        embed.set_footer(text=bot.user.name+"#"+bot.user.discriminator, icon_url=bot.user.avatar_url)

        self.embed = embed

    async def send(self, channel):
        return await channel.send(embed=self.embed)

    async def getrawembed(self):
        return self.embed
