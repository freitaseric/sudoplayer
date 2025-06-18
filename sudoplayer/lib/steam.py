import aiohttp

from functools import singledispatch
from typing import Any

from sudoplayer.lib.currency import get_brl_currency_values
from sudoplayer.lib.log import logger

GET_APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
GET_APP_DETAIL_URL = "https://store.steampowered.com/api/appdetails?appids="


def _is_valid_app(app: dict) -> bool:
    name = app.get("name", "").lower()
    excluded_terms = [
        "dedicated server",
        "dlc",
        "soundtrack",
        "ost",
        "server",
        "steam",
        "steam client",
        "steamworks common redistributables",
        "test app",
        "trailer",
        "editor",
        "tool",
        "demo",
    ]
    return not any(term in name for term in excluded_terms)


async def _exchange_app_price(app: dict) -> dict:
    """
    Exchanges the app price to a more readable format.
    This function now correctly handles free-to-play games.
    """
    if "price_overview" in app:
        price_overview = app["price_overview"]

        if price_overview.get("currency") != "BRL":
            brl_values = await get_brl_currency_values()
            exchange_factor = brl_values.get(price_overview["currency"].lower(), 1)

            initial_price = price_overview.get("final", 0)

            new_price = int(initial_price / exchange_factor)

            price_overview["final_formatted"] = f"R$ {new_price / 100:.2f}"

    return app


async def get_app_list() -> list[dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(GET_APP_LIST_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    apps = data.get("applist", {}).get("apps", [])
                    filtered_apps = [app for app in apps if _is_valid_app(app)]
                    return filtered_apps
                else:
                    logger.exception(f"Error fetching app list: {response.status}")
                    return []
        except aiohttp.ClientError as e:
            logger.exception(f"Client error fetching app list: {e}")
            return []


@singledispatch
async def get_app_details(appid_or_name: str | int) -> dict[str, Any] | None:
    raise TypeError(f"Unsupported type: {type(appid_or_name)}. Expected str or int.")


@get_app_details.register(int)
async def _(appid: int) -> dict[str, Any] | None:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{GET_APP_DETAIL_URL}{appid}") as response:
                if response.status == 200:
                    data = await response.json()
                    if str(appid) in data and data[str(appid)]["success"]:
                        app_data = data[str(appid)]["data"]
                        return await _exchange_app_price(app_data)
                    else:
                        logger.warning(
                            f"App ID {appid} not found or not successful in response."
                        )
                        return None
                else:
                    logger.exception(f"Error fetching app details: {response.status}")
                    return None
        except aiohttp.ClientError as e:
            logger.exception(f"Client error fetching details for appid {appid}: {e}")
            return None


@get_app_details.register(str)
async def _(name: str) -> dict[str, Any] | None:
    apps = await get_app_list()
    if not apps:
        return None

    for app in apps:
        if app["name"].lower() == name.lower():
            return await get_app_details(app["appid"])

    logger.warning(f"App with name '{name}' not found in the app list.")
    return None
