import asyncio
import contextlib
import logging
from pathlib import Path

from discord import Activity, ActivityType, Intents, Status
import discord
from discord.ext.commands import Bot as BotBase

from sudoplayer.core import env

COGS_PACKAGE = "sudoplayer.app.cogs"

_logger = logging.getLogger(__name__)


class Bot(BotBase):
    def __init__(self):
        intents = Intents.default()

        super().__init__(command_prefix="/", intents=intents)

        assert env.BOT_TOKEN
        self.token = env.BOT_TOKEN

        discord.utils.setup_logging()

    async def on_connect(self):
        """
        This method is called when the bot connects to Discord.
        """
        _logger.info("Discord client connected successfully!")
        await self.change_presence(
            activity=Activity(type=ActivityType.playing, name="Borderlands 3"),
            status=Status.idle,
        )

    async def setup_hook(self):
        _logger.info("Loading cogs...")
        cogs_path = Path(__file__).parent / ".." / "app" / "cogs"

        for file in cogs_path.glob("*.py"):
            if file.name.startswith("__"):
                continue

            cog_module = f"{COGS_PACKAGE}.{file.stem}"
            try:
                await self.load_extension(cog_module)
                _logger.debug(f"> Cog '{file.stem}' successfully loaded.")
            except Exception as e:
                _logger.exception(f"Error while loading cog {file.stem}: {e}")

        try:
            synced = await self.tree.sync()
            _logger.info(f"{len(synced)} commands syncronized.")
        except Exception as e:
            _logger.exception(f"Error while syncing the commands: {e}")

    async def main(self) -> None:
        async with self:
            await self.start(self.token)

    def starter(self):
        with contextlib.suppress(KeyboardInterrupt):
            asyncio.run(self.main())
