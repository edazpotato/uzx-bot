import os
import typing
import asyncio
import discord
from discord.ext import commands
from bot.custom import embeds


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xed3102

    @commands.command(name="purge", aliases=["clear", "delete", "del"])
    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_messages=True))
    @commands.bot_has_permissions(manage_messages=True)
    async def purge_messages_command(self, ctx, amount: typing.Optional[int] = 1):
        await ctx.channel.purge(limit=amount+1)
        msg = await ctx.send(f"Cleared {amount} messages")
        await asyncio.sleep(1)
        await msg.delete()

    @commands.command(name="ban")
    @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
    @commands.bot_has_permissions(ban_members=True)
    async def ban_member_command(self, ctx, member: discord.User = None, *, reason: str = "They were naughty"):
        if member == None:
            await ctx.send("I can't ban nothing...")
        elif member == ctx.message.author:
            await ctx.send("🤦")
        elif member == ctx.me:
            await ctx.send("no")
        elif member == self.bot.owner_id:
            await ctx.send("**Achivement get!**\n*discover an un-bannable user*")
        elif member.bot is False:
            DMmessage = f"**OOF!**\n You have been banished from `{ctx.guild.name}` because '`{reason}`'"
            await member.send(DMmessage)
        else:
            tag = f"{member.name}#{member.discriminator}"
            id = member.id
            await ctx.guild.ban(member, reason=reason)
            await ctx.channel.send(f"`{tag}`(`{id}`) got banned because {reason}!")
            #await ctx.guild.ban
            msg = await ctx.send(f"banned {member} for `{reason}`")
            await asyncio.sleep(1)
            await msg.delete()


    @commands.command(name="unban")
    @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
    @commands.bot_has_permissions(ban_members=True)
    async def unban_member_command(
            self, ctx,
            memberid: discord.User
    ):
        member = discord.Object(id=memberid)
        print(member)
        await ctx.guild.unban(member)
        data = {
            "title": "**Unban**",
            "color": self.color,
            "fields": [
                {
                    "title": "Member: ",
                    "content": "{0}#{1} (*{2}*)".format(member.name, member.discriminator, member.id),
                    "inline": True
                },
                {
                    "title": "Moderator: ",
                    "content": "{0}#{1} (*{2}*)".format(ctx.author.name, ctx.author.discriminator, ctx.author.id),
                    "inline": True
                }
            ]
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_guild=True))
    @commands.command(name="leave", aliases=["goaway"])
    async def leave_command(self, ctx):
        await ctx.message.add_reaction("👋")
        await ctx.send("'igt, ima head out ")
        await ctx.guild.leave()
