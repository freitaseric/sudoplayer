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
        await interaction.response.send_message(
            embed=embeds.default("Calculando a latência..."),
        )
        latency = round(self.bot.latency * 1000)
        embed = embeds.default(f"Latência: `{latency}ms`")
        await interaction.edit_original_response(embed=embed)

    @ping.error
    async def ping_error(self, interaction: Interaction, error: Exception):
        await interaction.response.send_message(
            embed=embeds.error(error), ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
