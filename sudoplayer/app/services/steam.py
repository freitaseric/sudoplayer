from datetime import datetime
import json
import logging
import aiohttp

from typing import Any, Optional

import redis

from sudoplayer.app.database import cache
from sudoplayer.app.services import CurrencyService
from sudoplayer.core import constants

GET_APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
GET_APP_DETAIL_URL = "https://store.steampowered.com/api/appdetails?appids="

STEAM_APP_LIST_CACHE_KEY = "steam:app_list"
STEAM_APP_DETAILS_CACHE_KEY = "steam:app_details"

_logger = logging.getLogger(__name__)


class SteamService:
    @staticmethod
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

    @staticmethod
    async def _get_cache(key: str) -> Optional[str]:
        data = await cache.get(key)
        if not data:
            _logger.warning(f"No cache found for key: {key}")
            return None

        return data

    @staticmethod
    async def _set_cache(key: str, data: str):
        created_at = datetime.now().isoformat()
        try:
            async with cache.pipeline() as pipe:
                await pipe.set(key, data, ex=1 * constants.DAYS)
                await pipe.set(f"{key}:created_at", created_at)
                await pipe.execute()
        except redis.RedisError as e:
            _logger.exception(
                f"Error while trying to set the data for key {key} to the cache: {e}"
            )

    @staticmethod
    async def _exchange_app_price(app: dict) -> dict:
        if "price_overview" in app:
            price_overview = app["price_overview"]

            old_price = price_overview.get("final", 0)
            origin_currency = price_overview.get("currency", "brl")

            new_price = await CurrencyService.convert_to_brl(old_price, origin_currency)

            price_overview["final_formatted"] = f"R$ {new_price / 100:.2f}"

        return app

    @staticmethod
    async def fetch_app_list() -> list[dict[str, Any]]:
        cached_data = await SteamService._get_cache(STEAM_APP_LIST_CACHE_KEY)
        if cached_data:
            return json.loads(cached_data)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(GET_APP_LIST_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        apps = data.get("applist", {}).get("apps", {})
                        apps = [app for app in apps if SteamService._is_valid_app(app)]
                        await SteamService._set_cache(
                            STEAM_APP_LIST_CACHE_KEY, json.dumps(apps)
                        )
                        return apps
                    else:
                        _logger.warning(
                            f"Error while trying to fetch steam app list with code: {response.status}"
                        )
                        return []

            except aiohttp.ClientError as e:
                _logger.exception(
                    f"Client error while trying to fetch steam app list: {e}"
                )
                return []

    @staticmethod
    async def fetch_app_details(appid: int) -> Optional[dict[str, Any]]:
        cached_data = await SteamService._get_cache(
            f"{STEAM_APP_DETAILS_CACHE_KEY}:{appid}"
        )
        if cached_data:
            return json.loads(cached_data)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{GET_APP_DETAIL_URL}{appid}") as response:
                    if response.status == 200:
                        data = await response.json()
                        if str(appid) in data and data[str(appid)]["success"]:
                            app_data = data[str(appid)]["data"]
                            app_data = await SteamService._exchange_app_price(app_data)
                            await SteamService._set_cache(
                                f"{STEAM_APP_DETAILS_CACHE_KEY}:{appid}",
                                json.dumps(app_data),
                            )
                            return app_data
                        else:
                            _logger.warning(
                                f"Steam app with id '{appid}' not found or not exists."
                            )
                            return None
                    else:
                        _logger.error(
                            f"Error while trying to fetch steam app list with code: {response.status}"
                        )
                        return None
            except aiohttp.ClientError as e:
                _logger.exception(
                    f"Client error while trying to fetch steam app details: {e}"
                )
                return None
