import asyncio
import discord
from discord.ext import commands

"""Contains the paginator class and the help cog."""


"""Dictionaries containing a list of commands and their description, TODO: maybe make a separate json file for them?"""

fun_cat_page = {"draw": "Draws a number between 0-100",
                "xkcd": "Get some random comic from xkcd",
                "reverse <something>": "Reverse a given message",
                "say <something>": "Echos a given message"
                }

utility_cat_page = {"lmgtfy <something>": "Returns an LMGTFY link", #TODO: this
                    "weather <somewhere>": "Returns the weather info of a given place", #TODO: this
                    "time <somewhere>": "Returns the time of a given place", #TODO: this
                    "pfp [user]": "Gets a user's profile picture", #done
                    "serverinfo": "Shows the current server's info", #done
                    "userinfo [user]": "Shows a user's info", #done
                    "stats": "Returns the bot's current stats",
                    "invite": "Returns this bot's invite link" #TODO: this
                    }

osu_cat_page = {"osu!link <account>": "Links your osu! account", #TODO: this
                "osu!stats [gamemode] [username]": "Returns a given user's osu! stats", #TODO: this
                "osu!recent [username]": "Returns the user's most recent score", #TODO: this
                "osu!score <map> [username]": "Returns a user's score on a map" #TODO: this
               }

fn_cat_page = {} 

admin_cat_page = {"ban <user>": "Bans a user from this server given the bot has permission to do so", #done
                  "kick <user>": "Kicks a user from this server given the bot has permission to do so", #done
                  "purge <message_count>": "Purges a given ammount of messages", #TODO: this
                  "mute <user>": "Mutes a user from this server" #TODO: this
                 }

conf_cat_page = {"set_prefix <prefix>": "Sets a custom prefix to this server", #TODO: requires some more testing
                 "config": "Start the bot configuration process" #TODO: this
                 #TODO: more commands?
                }

class Paginator:
    def __init__(self, ctx, channel, user, pages):
        self.ctx = ctx
        self.channel = channel
        self.message = None
        self.pages = pages
        self.length = len(pages)
        self.page = 0
        self.user = user
        Paginator.instance = self

    @staticmethod
    def reactions_check(reaction, user):
        if (user == Paginator.instance.user and str(reaction.emoji) == '⬅️'): return True
        if (user == Paginator.instance.user and str(reaction.emoji) == '⏹'): return True
        if (user == Paginator.instance.user and str(reaction.emoji) == '➡️'): return True
        if (user == Paginator.instance.user and str(reaction.emoji) == '❎'): return True

    
    async def start(self):
        if not self.channel.permissions_for(self.channel.guild.me).manage_messages:
           await self.user.send("Sorry, i do not have the manage message permission, so you can't use this command, please give it to me or use `.s help -o` instead or use `.s help -h` for more info")
           return
        if not self.channel.permissions_for(self.channel.guild.me).add_reactions:
           await self.ctx.send("Sorry, i do not have the permission to add reactions on this channel, please give it to me or use `.s help -o` instead or use `.s help -h` for more info")
           return
        else:
            self.message = await self.ctx.send(embed=self.pages[0])
            
        await self.message.add_reaction("⬅️")
        await self.message.add_reaction("⏹")
        await self.message.add_reaction("➡️")
        await self.message.add_reaction("❎")

        try:
            while True:
                reaction, user = await self.ctx.bot.wait_for('reaction_add', timeout=60, check=Paginator.reactions_check)
                if (user == self.user and str(reaction.emoji) == '⬅️'): 
                    await self.scroll_left()
                    await self.message.remove_reaction('⬅️', user)
                elif (user == self.user and str(reaction.emoji) == '⏹'): 
                    await self.stop()
                    await self.message.remove_reaction('⏹', user)
                    break
                elif (user == self.user and str(reaction.emoji) == '➡️'): 
                    await self.scroll_right()
                    await self.message.remove_reaction('➡️', user)
                elif (user == self.user and str(reaction.emoji) == '❎'):
                    await self.delete()
                    break
            
        except asyncio.TimeoutError:
            await self.message.clear_reactions()

    async def stop(self):
        await self.message.clear_reactions()

    async def delete(self):
       await self.message.delete()
 
    async def scroll_right(self):
        if self.page + 1 == self.length:
            self.page = 0
        else:
            self.page += 1

        await self.message.edit(embed=self.pages[self.page])
 
    async def scroll_left(self):
        if self.page == 0:
            self.page = self.length-1
        else:
            self.page -= 1
 
        await self.message.edit(embed=self.pages[self.page])

#TODO: fix bug with help command
class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.ctx = bot

    @commands.command()
    async def help(self, ctx, *, arg: str = None):
        fcp = discord.Embed(title='Fun Category:\n', colour=0x0d919c, description="\n".join([f"`{key}`: {value}" for (key, value) in fun_cat_page.items()]))
        acp = discord.Embed(title='Admin Category:\n', colour=0x0d919c, description="\n".join([f"`{key}`: {value}" for (key, value) in admin_cat_page.items()]))
        menu = Paginator(ctx, ctx.message.channel, ctx.author, [acp, fcp])
        await menu.start()

def setup(bot):
    bot.add_cog(HelpMenu(bot))
