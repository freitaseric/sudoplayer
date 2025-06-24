from datetime import datetime
from typing import Any
import discord

from sudoplayer.core import constants


class _GoToPageModal(discord.ui.Modal, title="Ir para página"):
    def __init__(self, app_list):
        super().__init__(timeout=600)

        self.app_list = app_list

    page = discord.ui.TextInput(
        label="Número da página",
        placeholder="Digite o número da página que deseja ir",
        min_length=1,
        max_length=7,
        required=True,
        style=discord.TextStyle.short,
    )

    async def on_submit(self, interaction: discord.Interaction):
        steam_app_list_view = SteamAppListView(self.app_list, interaction.user.id)

        try:
            page_number = int(self.page.value)
        except ValueError:
            embed = discord.Embed(
                title=f"{constants.CANCEL} | Ops, algo deu errado...",
                description="Por favor, insira um número válido.",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True,
            )
            return

        total_pages = len(self.app_list) // steam_app_list_view.items_per_page
        if not (0 <= page_number <= total_pages):
            embed = discord.Embed(
                title=f"{constants.CANCEL} | Ops, algo deu errado...",
                description=f"Por favor, insira um número de página entre 1 e {total_pages + 1}.",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True,
            )
            return

        steam_app_list_view.current_page = page_number
        steam_app_list_view.update_buttons()

        await interaction.response.edit_message(
            embed=steam_app_list_view.create_embed(),
            view=steam_app_list_view,
        )

        embed = discord.Embed(
            title=f"{constants.CHECK} | Sucesso!",
            description=f"Você foi redirecionado para a página {page_number}.",
            color=discord.Color.brand_green(),
            timestamp=datetime.now(),
        )

        await interaction.followup.send(
            embed=embed,
            ephemeral=True,
        )


class SteamAppListView(discord.ui.View):
    def __init__(self, app_list: list[dict[str, Any]], author_id: int, timeout=600):
        super().__init__(timeout=timeout)
        self.app_list = app_list
        self.current_page = 0
        self.items_per_page = 10
        self.author_id = author_id  # Salva o ID do autor
        self.update_buttons()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.author_id is not None and interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Apenas quem executou o comando pode usar estes botões.",
                ephemeral=True,
            )
            return False
        return True

    def create_embed(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_apps = self.app_list[start:end]

        embed = discord.Embed(
            title=f"{constants.STEAM} | Lista de Jogos do Steam",
            description=f"Foram encontrados um total de **{len(self.app_list)} jogos** no catálogo.\nUse `/jogo pesquisar <app_id>` ou `/jogo pesquisar <nome>` para buscar um jogo específico.",
            color=discord.Color.teal(),
        )
        for app in page_apps:
            embed.add_field(
                name=app["name"],
                value=f"App ID: {app['appid']}",
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

    @discord.ui.button(
        label="Primeira", style=discord.ButtonStyle.secondary, emoji="⏪"
    )
    async def first_page(self, interaction: discord.Interaction, _: discord.ui.Button):
        self.current_page = 0
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.primary, emoji="⬅️")
    async def prev_page(self, interaction: discord.Interaction, _: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Ir para", style=discord.ButtonStyle.secondary, emoji="🔍")
    async def go_to_page(self, interaction: discord.Interaction, _: discord.ui.Button):
        modal = _GoToPageModal(self.app_list)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Próxima", style=discord.ButtonStyle.primary, emoji="➡️")
    async def next_page(self, interaction: discord.Interaction, _: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Última", style=discord.ButtonStyle.secondary, emoji="⏩")
    async def last_page(self, interaction: discord.Interaction, _: discord.ui.Button):
        self.current_page = len(self.app_list) // self.items_per_page
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
