import discord
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ban(self, ctx, p_user: discord.Member, *, reason = None):
        user = self.bot.get_user(int(p_user)) if type(p_user) is str else p_user
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user} was banned successfully" + ("", f", Reason `{reason}`")[reason != None])

    @commands.command()
    async def kick(self, ctx, p_user: discord.Member, *, reason = None):
        user = self.bot.get_user(int(p_user)) if type(p_user) is str else p_user
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"{user} was kicked successfully" + ("", f", Reason: `{reason}`")[reason != None])

    """Error handlers"""
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("User not found")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a user to kick")
            return
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("I don't have the permissions to kick this user!")
            return
            
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("User not found")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a user to ban")
            return
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("I don't have the permissions to ban this user!")
            return

def setup(bot):
    bot.add_cog(AdminCog(bot))