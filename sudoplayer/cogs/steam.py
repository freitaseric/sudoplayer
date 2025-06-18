from datetime import datetime
from typing import Any
from discord.ext import commands
from discord import app_commands
import discord

from sudoplayer.lib import steam
from sudoplayer.utils import embeds


class Paginator(discord.ui.View):
    def __init__(self, app_list, timeout=180):
        super().__init__(timeout=timeout)
        self.app_list = app_list
        self.current_page = 0
        self.items_per_page = 10  # You can adjust this value
        self.update_buttons()

    def create_embed(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_apps = self.app_list[start:end]

        embed = discord.Embed(
            title="Lista de Jogos do Steam",
            description="Use `/jogo pesquisar <app_id>` ou `/jogo pesquisar <nome>` para buscar um jogo específico.",
            color=discord.Color.blurple(),
        )
        for app in page_apps:
            embed.add_field(
                name=app["name"],
                value=f"App ID: {app['appid']}",
                inline=True,
            )
        embed.set_footer(
            text=f"Página {self.current_page + 1}/{len(self.app_list) // self.items_per_page + 1}",
        )
        return embed

    def update_buttons(self):
        self.first_page.disabled = self.current_page == 0
        self.prev_page.disabled = self.current_page == 0
        self.next_page.disabled = self.current_page >= (
            len(self.app_list) // self.items_per_page
        )
        self.last_page.disabled = self.current_page >= (
            len(self.app_list) // self.items_per_page
        )

    @discord.ui.button(label="Primeira", style=discord.ButtonStyle.primary, emoji="⏪")
    async def first_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_page = 0
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.primary, emoji="⬅️")
    async def prev_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Próxima", style=discord.ButtonStyle.primary, emoji="➡️")
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Última", style=discord.ButtonStyle.primary, emoji="⏩")
    async def last_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_page = len(self.app_list) // self.items_per_page
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)


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

        if app_id is not None:
            if not isinstance(app_id, int):
                return await interaction.followup.send(
                    embed=embeds.error("O ID do jogo deve ser um número inteiro."),
                )

            app_details = await steam.get_app_details(app_id)
            if not app_details:
                return await interaction.followup.send(
                    embed=embeds.error(f"Jogo com ID {app_id} não encontrado."),
                )

            return await interaction.followup.send(
                embed=self._create_game_embed(app_details)
            )

        if name is not None:
            if not isinstance(name, str):
                return await interaction.followup.send(
                    embed=embeds.error("O nome do jogo deve ser uma string."),
                )

            name = name.strip()
            if not name:
                return await interaction.followup.send(
                    embed=embeds.error("O nome do jogo não pode estar vazio."),
                )

            app_details = await steam.get_app_details(name)
            if not app_details:
                return await interaction.followup.send(
                    embed=embeds.error(f"Jogo com nome '{name}' não encontrado."),
                )

            return await interaction.followup.send(
                embed=self._create_game_embed(app_details)
            )

        app_list = await steam.get_app_list()
        if not app_list:
            await interaction.followup.send(
                embed=embeds.error("Não foi possível obter a lista de jogos do Steam."),
            )
            return

        paginator = Paginator(app_list)
        return await interaction.followup.send(
            embed=paginator.create_embed(),
            view=paginator,
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
