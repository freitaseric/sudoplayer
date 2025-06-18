from sudoplayer.lib.log import logger


CURRENCY_BRL_API_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/brl.json"


async def get_brl_currency_values() -> dict[str, float]:
    import aiohttp

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(CURRENCY_BRL_API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["brl"]
                else:
                    logger.exception(
                        f"Failed to fetch BRL currency values: {response.status}"
                    )
                    return {}
        except aiohttp.ClientError as e:
            logger.exception(f"Error fetching BRL currency values: {e}")
            return {}
