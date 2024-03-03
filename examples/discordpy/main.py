import discord
from discord.ext import commands

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import os

COGS = ("cogs.vc_stats",)
TOKEN = os.environ.get("TOKEN", "")


class Bot(commands.Bot):
    def __init__(self):
        super().__init__("!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        for cog in COGS:
            await self.load_extension(cog)

    async def on_ready(self):
        if not self.user:
            return

        print("LOGIN")
        print(f"{self.user.name=}")
        print(f"{self.user.id=}")


if __name__ == "__main__":
    bot = Bot()
    bot.run(TOKEN)
