import asyncio
import contextlib
from pathlib import Path

from discord import Activity, ActivityType, Intents, Status
import discord
from discord.ext.commands import Bot as BotBase

from sudoplayer.lib.log import logger
from sudoplayer.config import env
from sudoplayer.utils import embeds

COGS_PACKAGE = "sudoplayer.cogs"


class Bot(BotBase):
    token = env.BOT_TOKEN

    def __init__(self):
        intents = Intents.default()

        super().__init__(command_prefix="/", intents=intents)

    async def on_connect(self):
        """
        This method is called when the bot connects to Discord.
        """
        logger.success("Discord client connected successfully!")
        await self.change_presence(
            activity=Activity(type=ActivityType.playing, name="Borderlands 3"),
            status=Status.idle,
        )

    async def on_error(self, event_method, *args, **kwargs):
        """
        This method is called when an error occurs in the bot.
        It logs the error with the event method name and arguments.
        """
        logger.error(f"An error occurred in {event_method}: {args} {kwargs}")

        webhook_url = env.ERROR_WEBHOOK_URL
        if not webhook_url:
            logger.warning("ERROR_WEBHOOK_URL variable is not set in your environment")
            return

        webhook = discord.Webhook.from_url(webhook_url)

        try:
            await webhook.edit(name="SudoPlayer Errors")
        except Exception:
            logger.warning("Invalid to customize the webhook error report")

        embed = embeds.custom(
            title="Error Report",
            description=f"An error occurred in `{event_method}`.",
            color=embeds.colors.ERROR,
        )
        embed.add_field(name="Arguments", value=str(args), inline=False)
        embed.add_field(name="Keyword Arguments", value=str(kwargs), inline=False)

        try:
            await webhook.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to send webhook: {e}")

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
