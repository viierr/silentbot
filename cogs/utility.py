# pylint: disable=F0401

import discord
from discord.ext import commands
import psutil, os
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta
from colorthief import ColorThief
import io

#TODO: learn how python imports work Lol
sys.path.append("../utils")
from utils.utils import utils



class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #TODO: bot uptime
    @commands.command(aliases=["bot_stats", "botinfo", "bot_info"])
    async def stats(self, ctx):
        em = discord.Embed(title="Bot statistics", color=0x0d919c)
        em.set_thumbnail(url=ctx.me.avatar_url)
        em.add_field(name="Owner", value="Owner: silentzer#9054", inline=False)
        em.add_field(name="Commands Prefix", value="`.s `", inline=False)
        em.add_field(name="Bot version", value="v2.0.0", inline=False)
        em.add_field(name="Servers", value=len(self.bot.guilds), inline=False)

        #TODO: read from json owner id
        if ctx.author.id == 236198462058790912:
            current_process = psutil.Process()
            em.add_field(name="CPU Usage:", value=f"{current_process.cpu_percent(interval=None):.2f} %", inline=False)
            em.add_field(name="RAM Usage:", value=f"{current_process.memory_full_info().uss / 1024 ** 2:.2f} MB / {psutil.virtual_memory().available / 1024 ** 2:.2f} MB", inline=False)
        
        await ctx.send(embed=em)
    
    @commands.command(aliases=["user_stats", "userstats", "user_info"])
    async def userinfo(self, ctx, p_user: discord.Member = None):
        user = p_user if p_user is not None else ctx.author

        rl_joined_at  =  relativedelta(datetime.now(), user.joined_at)
        rl_created_at =  relativedelta(datetime.now(), user.created_at)
    
        em = discord.Embed(title=f"{user.name}#{user.discriminator}" + ("", f" - {user.nick}")[user.nick != None], color=user.color if user.color != discord.Color.default() else 0x0d919c)
        em.set_thumbnail(url=user.avatar_url)

        #setup userinfo
        em.add_field(name="Account created at:", value=f"{user.created_at.strftime('%Y-%m-%d %H:%M')} ({rl_created_at.years} Years {rl_created_at.months} Months {rl_created_at.days} Days)", inline=False)
        em.add_field(name="Joined at:", value=f"{user.joined_at.strftime('%Y-%m-%d %H:%M')} ({rl_joined_at.years} Years {rl_joined_at.months} Months {rl_joined_at.days} Days)", inline=False)
        em.add_field(name="Activity:", value=f"Playing {user.activities[0].name}", inline=False)

        if user.color != discord.Color.default():
            em.add_field(name="User color:", value=f"RGB: {user.color.to_rgb()} | HEX: {'#%02x%02x%02x' % user.color.to_rgb()}", inline=False)
        em.add_field(name="ID:", value=user.id)

        await ctx.send(embed=em)
    
    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member not found")

    @commands.command(aliases=["serverstats", "server_stats", "server_info"])
    async def serverinfo(self, ctx):               
        em = discord.Embed(title=ctx.guild.name, color=discord.Colour.from_rgb(*ColorThief(io.BytesIO(await ctx.guild.icon_url.read())).get_color()) if ctx.guild.icon_url else 0x0d919c) 
        em.set_thumbnail(url=ctx.guild.icon_url)
            
        em.add_field(name="Server owner:", value=f"{ctx.guild.owner.mention} ({ctx.guild.owner_id})", inline=False)
        em.add_field(name="Created at:", value=ctx.guild.created_at.strftime('%Y-%m-%d %H:%M'))
        em.add_field(name="ID:", value=ctx.guild.id, inline=False)
        em.add_field(name="Members count:", value=len(ctx.guild.members), inline=False)
        em.add_field(name="Channels count:", value=f"Text: {len(ctx.guild.text_channels)}\n Voice: {len(ctx.guild.voice_channels)}\nTotal: {len(ctx.guild.channels)}", inline=False)
        em.add_field(name="Server region:", value=ctx.guild.region, inline=False)
        em.add_field(name="Verification Level:", value=ctx.guild.verification_level, inline=False)

        if ctx.guild.description:
            em.add_field(name="Server description:", value=ctx.guild.description)

        await ctx.send(embed=em)
    
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        try:
            user = member if member else ctx.author
            em = discord.Embed(title=f"{user.name}'s Avatar", color=discord.Colour.from_rgb(*ColorThief(io.BytesIO(await user.avatar_url.read())).get_color()))
            em.set_image(url=user.avatar_url)
            await ctx.send(embed=em)
        except discord.ext.commands.errors.BadArgument:
            await ctx.send("Invalid member")
    
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member not found")

def setup(bot):
    bot.add_cog(UtilityCog(bot))