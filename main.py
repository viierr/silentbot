import json
import aiosqlite
import sqlite3
import discord
from discord.ext import commands


"""silentbot's src:
* this is wip
* only 60% is completed"""

#TODO: rearrange cogs in alphabetical order
extensions = [
              "cogs.help",
              "cogs.fun",
              "cogs.utility",
              "cogs.config",
              "cogs.admin"
            ]

class SilentBot(commands.Cog):
    def __init__(self):
        self.bot = commands.Bot(command_prefix=SilentBot.get_prefix, description='silentbot v2', case_insensitive=True)

        with open('data/credentials.json') as r_credentials:
           self.credentials = json.load(r_credentials)
        
        self.db_conn = None
        SilentBot.instance = self

    @staticmethod
    async def get_prefix(bot, message):
        try:

            async with SilentBot.instance.db_conn.execute(f"SELECT prefix FROM prefixes WHERE id={message.guild.id}") as cur:
                row = await cur.fetchone()
                prefix = row[0]
                return commands.when_mentioned_or(prefix)(bot, message)

        except:
            return commands.when_mentioned_or(".s ")(bot, message)

    @commands.Cog.listener()
    async def on_ready(self):
        self.db_conn = await aiosqlite.connect("data/database.db")
        await self.db_conn.execute("CREATE TABLE IF NOT EXISTS prefixes (id integer PRIMARY KEY, prefix text NOT NULL)")
        await self.db_conn.commit()

        print(f'\n\nLogged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}\nServers: {len(self.bot.guilds)}')
        await self.bot.change_presence(activity=discord.Game(name="v2"))
        print(f'Booted successfully.')

    def start(self):
        self.bot.remove_command("help")
        self.bot.add_cog(self)

        for extension in extensions:
            self.bot.load_extension(extension)

        self.bot.run(self.credentials["discord_test_token"], bot=True, reconnect=True)

if __name__ == "__main__":
    SilentBot().start()