from bot.cogs import eventListeners, httpLoops, funCommands, minecraftCommands, utilityCommands, moderationCommands, adminCommands
import typing


class CogLoader:
    def __init__(self, bot):
        self.bot = bot
        # Load cogs
        self.bot.add_cog(eventListeners.Events(self.bot))
        self.bot.add_cog(httpLoops.Loop(self.bot))
        # commands
        self.bot.add_cog(adminCommands.Admin(self.bot))
        self.bot.add_cog(moderationCommands.Moderation(self.bot))
        self.bot.add_cog(utilityCommands.Utility(self.bot))
        self.bot.add_cog(funCommands.Fun(self.bot))
        self.bot.add_cog(minecraftCommands.Minecraft(self.bot))

        # loops
        self.bot.add_cog(httpLoops.Loop(self.bot))
