from bot.cogs import eventListeners, httpLoops, funCommands, minecraftCommands, utilityCommands, moderationCommands, adminCommands
import typing


class CogLoader:
    def __init__(self, bot):
        self.bot = bot
        # Load cogs
        self.bot.add_cog(eventListeners.Events(self.bot))
<<<<<<< HEAD
        self.bot.add_cog(httpLoops.Loop(self.bot))
=======
        # commands
>>>>>>> 0e329c2b7fb03bf3c1a2aa1a6c660c9073e1dd9b
        self.bot.add_cog(adminCommands.Admin(self.bot))
        self.bot.add_cog(moderationCommands.Moderation(self.bot))
        self.bot.add_cog(utilityCommands.Utility(self.bot))
        self.bot.add_cog(funCommands.Fun(self.bot))
        self.bot.add_cog(minecraftCommands.Minecraft(self.bot))
<<<<<<< HEAD

=======
        # loops
        self.bot.add_cog(httpLoops.Loop(self.bot))
>>>>>>> 0e329c2b7fb03bf3c1a2aa1a6c660c9073e1dd9b
