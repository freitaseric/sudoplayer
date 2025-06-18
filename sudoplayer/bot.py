import asyncio
import contextlib
from pathlib import Path

from discord import Activity, ActivityType, Intents
from discord.ext.commands import Bot as BotBase
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandError
from sudoplayer.lib.log import logger
from sudoplayer.config import env

COGS_PACKAGE = "sudoplayer.cogs"


class Bot(BotBase):
    token = env.BOT_TOKEN

    def __init__(self):
        intents = Intents.all()

        super().__init__(command_prefix="!", intents=intents)

    async def on_connect(self):
        """
        This method is called when the bot connects to Discord.
        """
        logger.success("Discord client connected successfully!")
        await self.change_presence(
            activity=Activity(type=ActivityType.watching, name="/ajuda")
        )

    async def on_command_error(self, ctx: Context, exception: CommandError) -> None:
        await ctx.reply("deu erro aqui irmão")

    async def setup_hook(self):
        """
        This method scans the 'cogs' directory for Python files and loads them as cogs.
        """
        logger.info("Loading cogs...")
        cogs_path = Path(__file__).parent / "cogs"

        for file in cogs_path.glob("*.py"):
            if file.name.startswith("__"):
                continue

            cog_module = f"{COGS_PACKAGE}.{file.stem}"
            try:
                await self.load_extension(cog_module)
                logger.debug(f"> Cog '{file.stem}' successfully loaded.")
            except Exception as e:
                logger.exception(f"Error while loading cog {file.stem}: {e}")

        try:
            synced = await self.tree.sync()
            logger.info(f"{len(synced)} commands syncronized.")
        except Exception as e:
            logger.exception(f"Error while syncing the commands: {e}")

    async def main(self) -> None:
        """
        This method is the main entry point for the bot.
        It starts the bot and keeps it running until interrupted.
        """
        if self.token is None:
            logger.critical(
                "Bot token is not set. Please configure the BOT_TOKEN environment variable."
            )
            exit(1)

        async with self:
            await self.start(self.token)

    def starter(self):
        """
        This method is used to start the bot in a way that allows for graceful shutdown.
        It runs the main method in an asyncio event loop and suppresses KeyboardInterrupt exceptions.
        """
        with contextlib.suppress(KeyboardInterrupt):
            asyncio.run(self.main())
