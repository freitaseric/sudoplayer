import logging


CURRENCY_BRL_API_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/brl.json"


_logger = logging.getLogger(__name__)


class CurrencyService:
    @staticmethod
    async def _get_brl_currency_values() -> dict[str, float]:
        import aiohttp

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(CURRENCY_BRL_API_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["brl"]
                    else:
                        _logger.warning(
                            f"Failed to fetch BRL currency values: {response.status}"
                        )
                        return {}
            except aiohttp.ClientError as e:
                _logger.exception(f"Error fetching BRL currency values: {e}")
                return {}

    @staticmethod
    async def convert_to_brl(value: float, origin_currency: str) -> float:
        origin_currency = origin_currency.lower()

        brl_values = await CurrencyService._get_brl_currency_values()
        exchange_factor = brl_values.get(origin_currency, 1.0)

        return value / exchange_factor
