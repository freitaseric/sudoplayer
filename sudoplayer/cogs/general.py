import discord
from discord.ext import commands
from discord import app_commands, Interaction

from sudoplayer.utils import embeds
from sudoplayer.lib.redis import r
import time


class General(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Responde com a latência do bot.")
    @app_commands.describe()
    async def ping(self, interaction: Interaction):
        bot_latency = round(self.bot.latency * 1000)

        start = time.perf_counter()
        await r.ping()
        redis_latency = round((time.perf_counter() - start) * 1000)

        await interaction.response.send_message(
            embed=embeds.custom(
            title="🏓 | Pong!",
            description=(
                f"🤖 | A latência do **bot** é de `{bot_latency}ms`.\n"
                f"🗄️ | A latência do **servidor cache** é de `{redis_latency}ms`."
            ),
            color=discord.Color.brand_green(),
            )
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
