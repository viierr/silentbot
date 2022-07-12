# pylint: disable=F0401

import discord
from discord.ext import commands
import random
import sys
sys.path.append("../utils")
from utils.utils import utils

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.ctx = bot
    
    @commands.command(aliases=["echo"])
    async def say(self, ctx, *, arg: str):
        """Echos a given message"""
        try:
            await ctx.send(arg)
        except:
            pass
    
    @commands.command()
    async def reverse(self, ctx, *, arg: str):
        """Reverses a given message"""
        try:
            await ctx.send(arg[::-1])
        except:
            pass
    
    @commands.command(aliases=["roll"])
    async def draw(self, ctx):
        """Draws a number between 0-100"""
        await ctx.send("Result: " + str(random.randint(0, 100)))
    
    @commands.command()
    async def xkcd(self, ctx):
        """Returns a random comic from xkcd"""
        #TODO: make async_return a list of responses maybe?
        req1 = await utils.async_get("https://c.xkcd.com/random/comic")
        req2 = await utils.async_get(str(req1.url) + "info.0.json")
        req_json = req2.json()
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.set_image(url=req_json['img'])
        em.set_author(name=req_json['alt'], url=req_json['img'])
        em.set_footer(text="Title: " + req_json['title'])
        await ctx.send(embed=em)
        

def setup(bot):
    bot.add_cog(FunCog(bot))

