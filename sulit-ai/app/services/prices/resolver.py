
from typing import Any

from app.services.prices.formatter import MARKET_DATASETS
from app.tools.psa_prices import fetch_psa_metadata
from app.services.prices.psa_client import find_commodity_codes


async def resolve_commodity_datasets(
    prompt: str,
) -> list[tuple[str, dict[str, Any], list[str]]]:
    """Return datasets containing commodities matched in the prompt."""
    matches = []

    for dataset_key, dataset in MARKET_DATASETS.items():
        metadata = await fetch_psa_metadata(dataset)

        commodity_codes = find_commodity_codes(prompt, metadata)

        if commodity_codes:
            matches.append(
                (dataset_key, metadata, commodity_codes)
            )

    return matches
