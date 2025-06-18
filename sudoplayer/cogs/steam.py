from datetime import datetime
from typing import Any
from discord.ext import commands
from discord import app_commands
import discord

from sudoplayer.lib import steam
from sudoplayer.utils import embeds
from sudoplayer.views.steam_app_list import SteamAppListView


class Steam(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    jogo = app_commands.Group(
        name="jogo",
        description="Interagir com jogos do Steam",
    )

    @jogo.command(
        name="pesquisar",
        description="Pesquisar jogos no Steam",
    )
    @app_commands.describe(app_id="ID do jogo no Steam", name="Nome do jogo")
    async def game_search(
        self,
        interaction: discord.Interaction,
        app_id: int | None = None,
        name: str | None = None,
    ):
        """
        Command to interact with Steam games.
        """

        await interaction.response.defer(thinking=True)

        if app_id is None and name is None:
            app_list = await steam.get_app_list()
            if not app_list:
                return await interaction.followup.send(
                    embed=embeds.error(
                        "Não foi possível obter a lista de jogos do Steam."
                    ),
                )

            view = SteamAppListView(app_list, interaction.user.id)
            return await interaction.followup.send(embed=view.create_embed(), view=view)

        query = app_id if app_id is not None else name

        app_details = await steam.get_app_details(query)
        if not app_details:
            return await interaction.followup.send(
                embed=embeds.error(
                    f"Não foi possível obter uma resposta para '{query}'."
                )
            )

        return await interaction.followup.send(
            embed=self._create_game_embed(app_details)
        )

    def _create_game_embed(self, app_details: dict[str, Any]) -> discord.Embed:
        try:
            description = app_details.get(
                "short_description", "Sem descrição disponível."
            )
            if len(description) > 4096:
                description = description[:4093] + "..."

            embed = discord.Embed(
                title=app_details.get("name", "Jogo Steam"),
                description=description,
                color=discord.Color.blue(),
            )

            embed.add_field(
                name="App ID", value=app_details.get("steam_appid", "N/A"), inline=True
            )
            embed.add_field(
                name="Desenvolvedor",
                value=", ".join(app_details.get("developers", [])),
                inline=True,
            )
            embed.add_field(
                name="Publicadora",
                value=", ".join(app_details.get("publishers", [])),
                inline=True,
            )
            embed.add_field(
                name="Preço (Possivelmente impreciso)",
                value=app_details.get("price_overview", {}).get(
                    "final_formatted", "Gratuito"
                ),
                inline=True,
            )
            embed.add_field(
                name="Gêneros",
                value=", ".join(
                    [g["description"] for g in app_details.get("genres", [])]
                ),
                inline=True,
            )
            release_date_str = app_details.get("release_date", {}).get("date", None)
            if release_date_str:
                try:
                    release_date = datetime.strptime(release_date_str, "%d %b, %Y")
                    timestamp = int(release_date.timestamp())
                    embed.add_field(
                        name="Data de Lançamento",
                        value=f"<t:{timestamp}:D>",
                        inline=True,
                    )
                except ValueError:
                    embed.add_field(
                        name="Data de Lançamento",
                        value=release_date_str,
                        inline=True,
                    )
            else:
                embed.add_field(
                    name="Data de Lançamento",
                    value="N/A",
                    inline=True,
                )

            if app_details.get("header_image"):
                embed.set_image(url=app_details["header_image"])

            embed.set_footer(text="Dados fornecidos pela Steam")
        except Exception as e:
            embed = embeds.error(f"Erro ao criar embed: {str(e)}")
            embed.title = "Erro ao obter detalhes do jogo"

        return embed


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Steam(bot))
