import discord
from discord.ext import commands

class osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def link(self, ctx, *, username: str = None):
        if username is None:
            await ctx.send("No username specified")

        
def setup(bot):
    bot.add_cog(osu(bot))