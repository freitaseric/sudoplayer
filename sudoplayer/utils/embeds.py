import datetime
from functools import singledispatch
from typing import Optional
import discord
from sudoplayer.config import colors
from sudoplayer.config import emojis


def success(msg: str) -> discord.Embed:
    """
    Creates an embed with a success color.
    """
    return discord.Embed(description=f"{emojis.CHECK} | {msg}", color=colors.SUCCESS)


def default(msg: str) -> discord.Embed:
    """
    Creates an embed with an default color.
    """
    return discord.Embed(description=msg, color=colors.DEFAULT)


def warning(msg: str) -> discord.Embed:
    """
    Creates an embed with a warning color.
    """
    return discord.Embed(description=f"{emojis.WARNING} | {msg}", color=colors.WARNING)


def magic(msg: str) -> discord.Embed:
    """
    Creates an embed with a magic color.
    """
    return discord.Embed(description=f"{emojis.MAGIC} | {msg}", color=colors.MAGIC)


@singledispatch
def error(exceptionOrMsg) -> discord.Embed:
    """
    Creates an embed with an error color.
    """
    raise TypeError(
        f"Unsupported type: {type(exceptionOrMsg)}. Expected str or Exception."
    )


@error.register(str)
def _(msg: str) -> discord.Embed:
    return discord.Embed(description=f"{emojis.CANCEL} | {msg}", color=colors.ERROR)


@error.register(Exception)
def _(exception: Exception) -> discord.Embed:
    return discord.Embed(
        description=f"{emojis.CANCEL} | {exception.__str__()}",
        color=colors.ERROR,
    )


class EmbedAuthor:
    """
    A class to create an embed author with a name and icon.
    """

    def __init__(self, name: str, icon_url: Optional[str] = None):
        self.name = name
        self.icon_url = icon_url

    def to_dict(self) -> dict:
        return (
            {"name": self.name, "icon_url": self.icon_url}
            if self.icon_url
            else {"name": self.name}
        )


class EmbedFooter:
    """
    A class to create an embed footer with a text and icon.
    """

    def __init__(self, text: str, icon_url: Optional[str] = None):
        self.text = text
        self.icon_url = icon_url

    def to_dict(self) -> dict:
        return (
            {"text": self.text, "icon_url": self.icon_url}
            if self.icon_url
            else {"text": self.text}
        )


class EmbedField:
    """
    A class to create an embed field with a name and value.
    """

    def __init__(self, name: str, value: str, inline: bool = False):
        self.name = name
        self.value = value
        self.inline = inline

    def to_dict(self) -> dict:
        return {"name": self.name, "value": self.value, "inline": self.inline}


def custom(
    title: Optional[str] = None,
    description: Optional[str] = None,
    color: discord.Colour = colors.DEFAULT,
    author: Optional[EmbedAuthor] = None,
    thumbnail: Optional[str] = None,
    image: Optional[str] = None,
    footer: Optional[EmbedFooter] = None,
    fields: Optional[list[EmbedField]] = None,
    timestamp: datetime.datetime = datetime.datetime.now(),
) -> discord.Embed:
    """
    Creates a custom embed with the given
    """
    embed = discord.Embed(
        title=title, description=description, color=color, timestamp=timestamp
    )

    if author:
        embed.set_author(**author.to_dict())
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    if footer:
        embed.set_footer(**footer.to_dict())
    if fields:
        for field in fields:
            embed.add_field(**field.to_dict())

    return embed
