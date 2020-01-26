import os
import json
import discord
import traceback
import asyncio

from collections import namedtuple
from discord.ext import commands

class Bot(commands.AutoShardedBot):
    """Custom extension of the AutoShardedBot provided by discord.py"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("./config.json", "r", encoding="utf8") as file: 
            data = json.dumps(json.load(file))
            self.config = json.loads(data, object_hook=lambda d: namedtuple("config", d.keys())(*d.values()))
            
    async def load_cogs(self):
        """Loads all the "cogs" of this bot. """
        modules = os.listdir('./modules')
        for module in modules:
            if module == '__pycache__' or module == '__init__.py':
                pass
            else:
                try:
                    module = module.replace(".py", "")
                    self.load_extension('modules.' + module)
                except Exception as e:
                    log = ("Exception in loading module '{}'\n"
                           "".format(module))
                    log += "".join(traceback.format_exception(type(e), e,
                                                              e.__traceback__))
                    print(log)


    async def on_ready(self):
        """Prints a message on ready."""
        print("Running.")
        await self.load_cogs()
        await self.change_presence(status=discord.Status.offline)



shell = Bot(command_prefix="!")