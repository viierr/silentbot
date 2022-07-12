# pylint: disable=no-name-in-module

from discord.ext import commands
import sys
sys.path.append("../")
from main import SilentBot

class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #TODO: prefix sanitization?
    @commands.command()
    async def set_prefix(self, ctx, *, prefix: str = None):
        """Sets a custom prefix on a server"""
        if prefix is None:
            await ctx.send("No prefix specified!")
            return
        if '"' in prefix:
            return
        try:
            await SilentBot.instance.db_conn.execute("INSERT OR REPLACE INTO prefixes (id, prefix) VALUES (?, ?)", (ctx.guild.id, prefix))
            await SilentBot.instance.db_conn.commit()
            await ctx.send("Prefix set successfully!")
            
        except Exception as e:
            await ctx.send("An error has occured!")
            print(e)

def setup(bot):
    bot.add_cog(ConfigCog(bot))