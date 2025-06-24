from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands, Interaction

import time

from sudoplayer.app.database import cache


class GeneralCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Responde com a latência do bot.")
    @app_commands.describe()
    async def ping(self, interaction: Interaction):
        bot_latency = round(self.bot.latency * 1000)

        start = time.perf_counter()
        await cache.ping()
        redis_latency = round((time.perf_counter() - start) * 1000)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="🏓 | Pong!",
                description=(
                    f"🤖 | A latência do **bot** é de `{bot_latency}ms`.\n"
                    f"🗄️ | A latência do **servidor cache** é de `{redis_latency}ms`."
                ),
                color=discord.Color.blurple(),
                timestamp=datetime.now(),
            )
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GeneralCog(bot))
