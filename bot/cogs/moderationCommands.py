import os
import typing
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
    async def purge_messages_command(
            self, ctx,
            members: commands.Greedy[discord.Member],
            amount: typing.Optional[int] = 1):
        def is_deletable(m):
            if members:
                return m.author in members
            else:
                return True
        ctx.channel.purge(limit=amount,check=is_deletable)
        cleared = ", ".join(x.name for x in members)
        await ctx.send("Cleared {0} messages from users: {1}".format(amount, cleared))

    @commands.command(name="ban")
    @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
    @commands.bot_has_permissions(ban_members=True)
    async def ban_member_command(
            self, ctx,
            member: typing.Union[discord.User, discord.Member],
            delete_days: typing.Optional[int] = 0,
            *,
            reason: typing.Optional[str] = "They were naughty"
    ):
        data = {
            "title": "**Ban**",
            "color": self.color,
            "fields": [
                {
                    "title": "Member: ",
                    "content": "Banned **{0}#{1}** (*{2}*)\n{3}".format(member.name, member.discriminator,
                                                                        member.id, member.mention),
                    "inline": True
                },
                {
                    "title": "Moderator: ",
                    "content": "{0}#{1} (*{2}*)".format(ctx.author.name, ctx.author.discriminator, ctx.author.id),
                    "inline": True
                },
                {
                    "blank": True,
                    "inline": False
                },
                {
                    "title": "Reason: ",
                    "content": reason,
                    "inline": True
                },
                {
                    "title": "Message deletion days: ",
                    "content": delete_days,
                    "inline": True
                }
            ]
        }
        embed = embeds.RichEmbed(self.bot, data)
        data2 = {
            "title": "**You were banned**",
            "color": self.color,
            "fields": [
                {
                    "title": "Server: ",
                    "content": "{0} (*{1}*)".format(ctx.guild.name, ctx.guild.id),
                    "inline": True
                },
                {
                    "title": "Moderator: ",
                    "content": "{0}#{1} (*{2}*)".format(ctx.author.name, ctx.author.discriminator, ctx.author.id),
                    "inline": True
                },
                {
                    "blank": True,
                    "inline": False
                },
                {
                    "title": "Reason: ",
                    "content": reason,
                    "inline": True
                },
                {
                    "title": "Message deletion days: ",
                    "content": delete_days,
                    "inline": True
                }
            ]
        }
        embed2 = embeds.RichEmbed(self.bot, data2)
        print(member)
        if hasattr(member, 'guild'):
            if member.id != self.bot.owner_id:
                await member.send(ctx.guild.get_member(member), embed=embed2.getrawembed())
                await member.ban(reason=reason, delete_message_days=delete_days)
                await embed.send(ctx.channel)

        else:
            if member != self.bot.owner_id:
                await self.bot.get_user(member).send(embed=embed2.getrawembed())
                await ctx.guild.ban(user=member, reason=reason, delete_message_days=delete_days)
                await embed.send(ctx.channel)

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

    @commands.check_any(commands.is_owner(), commands.has_permissions(kick_members=True))
    @commands.command(name="leave", aliases=["goaway"])
    async def leave_command(self, ctx):
        await ctx.message.add_reaction("😢")
        await ctx.send("😢")
        await ctx.send("'igt, ima head out 😢")
        await ctx.guild.leave()
