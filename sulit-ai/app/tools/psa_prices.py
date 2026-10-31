import logging
import re

from langchain_core.tools import tool

from app.services.prices.formatter import format_price_context
from app.services.prices.psa_client import psa_client
from app.services.prices.registry import PHILIPPINES_GEOLOCATION_CODE
from app.services.prices.resolver import month_codes, recent_year_codes, resolve_commodity_datasets

logger = logging.getLogger(__name__)
_PRICE_INTENT = re.compile(r"\b(price|prices|cost|costs|how much|market rate|market price|afford)\b", re.I)


async def get_price_context_for_prompt(prompt: str) -> str | None:
    if not _PRICE_INTENT.search(prompt):
        return None

    matches = await resolve_commodity_datasets(prompt)
    if not matches:
        return None

    contexts = []
    for dataset, metadata, commodity_codes in matches:
        selections = {
            "Geolocation": [PHILIPPINES_GEOLOCATION_CODE],
            "Commodity": commodity_codes,
            "Year": recent_year_codes(metadata),
            "Period": month_codes(metadata),
        }
        data = await psa_client.fetch_data(dataset, selections)
        context = format_price_context(dataset.key, data, metadata)
        if context:
            contexts.append(context)

    return "\n\n".join(contexts) if contexts else None


@tool
async def get_psa_prices(prompt: str) -> str:
    """Look up official PSA retail prices for the goods named in a price question."""
    try:
        return await get_price_context_for_prompt(prompt) or (
            "No matching PSA commodity prices were found for that request."
        )
    except Exception:
        logger.exception("PSA price lookup failed.")
        return "PSA price data is temporarily unavailable. Do not guess or invent a price."
