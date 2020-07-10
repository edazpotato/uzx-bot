from bot.cogs import eventListeners, httpLoops, funCommands, utilityCommands, moderationCommands, adminCommands


class CogLoader:
    def __init__(self, bot):
        self.bot = bot

    def loadcogs(self):
        # initialize cogs
        # event listeners
        self.bot.add_cog(eventListeners.Events(self.bot))
        # loops
        self.bot.add_cog(httpLoops.Loop(self.bot))
        # commands
        self.bot.add_cog(adminCommands.Admin(self.bot))
        self.bot.add_cog(moderationCommands.Moderation(self.bot))
        self.bot.add_cog(utilityCommands.Utility(self.bot))
        self.bot.add_cog(funCommands.Fun(self.bot))
