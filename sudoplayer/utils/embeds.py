from functools import singledispatch
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
