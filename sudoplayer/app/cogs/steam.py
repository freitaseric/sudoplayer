from datetime import datetime, time
from typing import Any
from discord.ext import commands, tasks
from discord import app_commands
import discord

from sudoplayer.app import database
from sudoplayer.app.services import SteamService
from sudoplayer.app.services.steam import STEAM_APP_DETAILS_CACHE_KEY
from sudoplayer.app.views import SteamAppListView
from sudoplayer.core import constants


async def game_search_autocomplete_name(
    _: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    app_list = await SteamService.fetch_app_list()
    if not app_list:
        return [
            app_commands.Choice(
                name="Não foi possível encontrar a lista de apps ¯\\_(ツ)_/¯",
                value="none",
            )
        ]

    if current == "":
        return [
            app_commands.Choice(name=app.get("name", ""), value=app.get("name", ""))
            for app in app_list
        ][:25]

    return [
        app_commands.Choice(name=app.get("name", ""), value=app.get("name", ""))
        for app in app_list
        if current.lower() in app.get("name", "").lower()
    ][:25]


class SteamCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(time=time(hour=0))
    async def fetch_steam_apps(self):
        return await SteamService.fetch_app_list()

    game = app_commands.Group(
        name="jogo",
        description="Interagir com jogos do Steam",
    )

    @game.command(
        name="listar", description="Lista todos os jogos disponíveis na Steam."
    )
    async def game_list(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        app_list = await self.fetch_steam_apps()

        if not app_list:
            embed = discord.Embed(
                title=f"{constants.CANCEL} | Ops, algo deu errado...",
                description="Não foi possível obter a lista de jogos da Steam!",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )

            return await interaction.followup.send(embed=embed)

        view = SteamAppListView(app_list, interaction.user.id)
        return await interaction.followup.send(embed=view.create_embed(), view=view)

    @game.command(
        name="pesquisar",
        description="Pesquisar jogos no Steam",
    )
    @app_commands.describe(name="Nome do jogo")
    @app_commands.autocomplete(name=game_search_autocomplete_name)
    async def game_search(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        await interaction.response.defer(thinking=True)

        app_list = await self.fetch_steam_apps()

        if not app_list:
            embed = discord.Embed(
                title=f"{constants.CANCEL} | Ops, algo deu errado...",
                description="Não foi possível obter a lista de jogos da Steam!",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )

            return await interaction.followup.send(embed=embed)

        appid = None
        name_lower = name.lower()
        for app in app_list:
            if app.get("name", "").lower() == name_lower:
                appid = app.get("appid")
                break

        if appid is None:
            embed = discord.Embed(
                title=f"{constants.CANCEL} | Ops, algo deu errado...",
                description=f"Não foi encontrado nenhum jogo chamado `{name}`.",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            return await interaction.followup.send(embed=embed)

        app_details = await SteamService.fetch_app_details(appid)
        if not app_details:
            embed = discord.Embed(
                title=f"{constants.CANCEL} | Ops, algo deu errado...",
                description=f"Não foi encontrado nenhum jogo chamado `{name}`.",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            return await interaction.followup.send(embed=embed)

        return await interaction.followup.send(
            embed=await self._create_game_embed(app_details)
        )

    async def _create_game_embed(self, app_details: dict[str, Any]) -> discord.Embed:
        try:
            description = app_details.get(
                "short_description", "Sem descrição disponível."
            )
            if len(description) > 4096:
                description = description[:4093] + "..."

            embed = discord.Embed(
                title=app_details.get("name", "Jogo Steam"),
                description=description,
                color=discord.Color.blurple(),
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

            thumbnail_url = app_details.get("screenshots", [])[0].get(
                "path_thumbnail", ""
            )
            embed.set_thumbnail(url=thumbnail_url)

            cache_created_at = await database.get_created_at(
                f"{STEAM_APP_DETAILS_CACHE_KEY}:{app_details.get('steam_appid', '')}"
            )
            embed.set_footer(
                text=f"Dados fornecidos pela Steam em {cache_created_at.strftime('%d/%m/%Y às %H:%M')}"
            )
        except Exception as e:
            embed = discord.Embed(
                title=f"{constants.CANCEL} | Ops, algo deu errado...",
                description=f"Erro ao criar embed: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
        return embed


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SteamCog(bot))
