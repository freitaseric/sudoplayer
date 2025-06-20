from datetime import datetime, time
import json
from typing import Any
from discord.ext import commands, tasks
from discord import app_commands
import discord

from sudoplayer.lib import steam
from sudoplayer.lib.redis import r
from sudoplayer.lib.log import logger
from sudoplayer.utils import embeds
from sudoplayer.views.steam_app_list import SteamAppListView

HOUR_IN_SECONDS = 60 * 60


async def game_search_autocomplete_name(
    _: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    app_list_string = await r.get("steam:app_list")
    app_list = json.loads(app_list_string) if app_list_string else None

    if not app_list:
        return [
            app_commands.Choice(
                name="Não foi possível encontrar a lista de apps ¯\\_(ツ)_/¯",
                value="none",
            )
        ]

    return [
        app_commands.Choice(name=app.get("name"), value=app.get("appid"))
        for app in app_list
        if current.lower() in app.get("name", "").lower()
    ]


async def game_search_autocomplete_appid(
    _: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    app_list_string = await r.get("steam:app_list")
    app_list = json.loads(app_list_string) if app_list_string else None

    if not app_list:
        return [
            app_commands.Choice(
                name="Não foi possível encontrar a lista de apps ¯\\_(ツ)_/¯",
                value="none",
            )
        ]

    return [
        app_commands.Choice(name=app.get("name"), value=app.get("appid"))
        for app in app_list
        if str(app.get("appid")).startswith(current)
    ]


class Steam(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(time=time(hour=0))
    async def fetch_steam_apps(self):
        app_list = await steam.get_app_list()
        if app_list:
            success = await r.set(
                "steam:app_list", json.dumps(app_list), ex=24 * HOUR_IN_SECONDS
            )
            if not success:
                logger.warning("Unable to set steam app list to cache.")
            return app_list

    game = app_commands.Group(
        name="jogo",
        description="Interagir com jogos do Steam",
    )

    @game.command(
        name="pesquisar",
        description="Pesquisar jogos no Steam",
    )
    @app_commands.describe(app_id="ID do jogo no Steam", name="Nome do jogo")
    @app_commands.autocomplete(app_id=game_search_autocomplete_appid)
    @app_commands.autocomplete(name=game_search_autocomplete_name)
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

        app_list_string = await r.get("steam:app_list")
        app_list = (
            json.loads(app_list_string)
            if app_list_string
            else await self.fetch_steam_apps()
        )
        if not app_list:
            return await interaction.followup.send(
                embed=embeds.error("Não foi possível obter a lista de jogos do Steam."),
            )

        if app_id is None and name is None:
            view = SteamAppListView(app_list, interaction.user.id)
            return await interaction.followup.send(embed=view.create_embed(), view=view)

        query = None
        if app_id is not None:
            query = app_id
        elif name is not None:
            name_lower = name.lower()
            for app in app_list:
                if app.get("name", "").lower() == name_lower:
                    query = app.get("appid")
                    break
            if query is None:
                return await interaction.followup.send(
                    embed=embeds.error(
                        f"Não foi encontrado nenhum jogo chamado `{name}`."
                    )
                )

        app_details_string = await r.get(f"steam:app_details:{query}")
        app_details = (
            json.loads(app_details_string)
            if app_details_string
            else await self._fetch_steam_app_details(query)
        )
        if not app_details:
            return await interaction.followup.send(
                embed=embeds.error(f"Não foi encontrado nenhum jogo com id `{query}`.")
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

    async def _fetch_steam_app_details(self, query: str | int | None):
        app_details = await steam.get_app_details(query)
        if app_details:
            await r.set(
                f"steam:app_details:{query}",
                json.dumps(app_details),
                ex=3 * HOUR_IN_SECONDS,
            )
        return app_details


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Steam(bot))
