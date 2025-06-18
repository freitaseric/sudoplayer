import discord
from discord.ext import commands
from discord import app_commands, Interaction

from sudoplayer.utils import embeds


class General(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Responde com a latência do bot.")
    @app_commands.describe()
    async def ping(self, interaction: Interaction):
        latency = round(self.bot.latency * 1000)

        await interaction.response.send_message(
            embed=embeds.custom(
                title="Pong!",
                description=f"🏓 | A latência do bot é de **{latency}ms**.",
                color=discord.Color.brand_green(),
            )
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
