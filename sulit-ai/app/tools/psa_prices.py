
import asyncio
import re
from typing import Any, Literal

import httpx
import logging

from langchain_core.tools import tool

from app.services.prices.formatter import MarketDataset

logger = logging.getLogger(__name__)
ResponseFormat = Literal["json", "csv", "json-stat", "json-stat2", "px"]

# PSA_URL = (
#     "https://openstat.psa.gov.ph/PXWeb/api/v1/en/"
#     "DB/2M/2018NEW/0042M4ARN10.px"
# )
PHILIPPINES_GEOLOCATION_CODE = "000000000"
_METADATA_CACHE: dict[str, Any] | None = None
_METADATA_LOCK = asyncio.Lock()
_PRICE_INTENT_PATTERN = re.compile(
    r"\b(price|prices|cost|costs|how much|market rate|market price|afford)\b",
    re.IGNORECASE,
)
_COMMODITY_NOISE_WORDS = {
    "fresh",
    "edible",
    "loose",
    "dressed",
    "whole",
    "kg",
    "pc",
},
_COMMODITY_LOCATOR: dict[int, str] = {
    0: "FRESH CHICKEN, BREAST, 1 KG",
    1: "FRESH CHICKEN, FULLY DRESSED, BROILER, 1 KG",
    2: "FRESH CHICKEN, LEGS, 1 KG",
    3: "FRESH CHICKEN, NATIVE, 1 KG",
    4: "FRESH CHICKEN, NATIVE, DRESSED, WHOLE, 1 KG",
    5: "FRESH CHICKEN, WHOLE, DRESSED, BOUNTY FRESH, 1 KG",
    6: "FRESH CHICKEN, WINGS, 1 KG",
    7: "EDIBLE OFFAL, FEET, CHICKEN, 1 KG",
    8: "EDIBLE OFFAL, GIZZARD, CHICKEN, 1 KG",
    9: "EDIBLE OFFAL, GIZZARD, MAGNOLIA, CHICKEN, 1 KG",
    10: "EDIBLE OFFAL, LIVER, CHICKEN, FRESH, 1 KG",
    11: "FRESH EGG, CHICKEN, MEDIUM, 1 PC",
    12: "FRESH EGG, CHICKEN, NATIVE, MEDIUM, 1 PC",
    13: "FRESH EGG, DUCK, MEDIUM, 1 PC",
    14: "FRESH EGG, QUAIL, LOOSE, 1 PC",
}
_GOODS_SEPARATOR_PATTERN = re.compile(r"\s*(?:,|/|&|\band\b)\s*", re.IGNORECASE)
_MONTH_ORDER = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def build_psa_query(selections: dict[str, list[str]], response_format: ResponseFormat = "json-stat",) -> dict:
    """Build a PXWeb query from dimension and category codes."""
    if not selections:
        raise ValueError("At least one dimension is required.")

    query = []

    for dimension, values in selections.items():
        if not values:
            raise ValueError(f"No values provided for {dimension}.")

        query.append({
            "code": dimension,
            "selection": {
                "filter": "item",
                "values": values,
            },
        })

    return {
        "query": query,
        "response": {"format": response_format},
    }


async def fetch_psa_data(
    dataset: MarketDataset,
    selections: dict[str, list[str]],
    response_format: ResponseFormat = "json",
) -> dict:
    """Fetch data from PSA. Not a LangChain tool."""
    payload = build_psa_query(selections, response_format)

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(dataset.url, json=payload)
        response.raise_for_status()
        return response.json()


async def fetch_psa_metadata(dataset: MarketDataset) -> dict[str, Any]:
    """Return the cached PXWeb table metadata used to resolve commodity names."""
    global _METADATA_CACHE

    if _METADATA_CACHE is not None:
        return _METADATA_CACHE

    async with _METADATA_LOCK:
        if _METADATA_CACHE is not None:
            return _METADATA_CACHE

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(dataset.url)
            response.raise_for_status()
            return response.json()

    return _METADATA_CACHE


def is_price_request(prompt: str) -> bool:
    """Return whether a prompt asks for price information."""
    return bool(_PRICE_INTENT_PATTERN.search(prompt))


def _normalise_words(value: str) -> set[str]:
    words = set(re.findall(r"[a-z]+", value.lower()))
    return {
        word[:-1] if len(word) > 3 and word.endswith("s") else word
        for word in words
        if word not in _COMMODITY_NOISE_WORDS
    }


def _get_dimension(metadata: dict[str, Any], code: str) -> dict[str, Any]:
    for variable in metadata.get("variables", []):
        if variable.get("code") == code:
            return variable
    raise ValueError(f"PSA metadata does not include the '{code}' dimension.")


def _find_best_commodity_codes(
    prompt_words: set[str],
    codes: list[str],
    names: list[str],
) -> list[str]:
    """Return the best matching catalog entries for one requested good."""
    matches: list[tuple[str, int]] = []

    for code, name in zip(codes, names, strict=True):
        commodity_words = _normalise_words(name)
        if "egg" in commodity_words and "egg" not in prompt_words:
            continue
        match_count = len(commodity_words & prompt_words)
        if match_count:
            matches.append((code, match_count))

    if not matches:
        return []

    highest_match_count = max(match_count for _, match_count in matches)
    return [code for code, match_count in matches if match_count == highest_match_count]


def find_commodity_codes(prompt: str, metadata: dict[str, Any]) -> list[str]:
    """Find PSA commodity codes for every good named in a price question."""
    commodity = _get_dimension(metadata, "Commodity")
    codes = commodity.get("values", [])
    names = commodity.get("valueTexts", [])

    matched_codes: list[str] = []
    for requested_good in _GOODS_SEPARATOR_PATTERN.split(prompt):
        for code in _find_best_commodity_codes(
            _normalise_words(requested_good), codes, names
        ):
            if code not in matched_codes:
                matched_codes.append(code)

    return matched_codes


def _get_recent_year_codes(metadata: dict[str, Any], year_count: int = 2) -> list[str]:
    year = _get_dimension(metadata, "Year")
    values = year.get("values", [])
    if not values:
        raise ValueError("PSA metadata has no year values.")
    return values[-year_count:]


def _get_month_codes(metadata: dict[str, Any]) -> list[str]:
    period = _get_dimension(metadata, "Period")
    return [
        code
        for code, name in zip(period.get("values", []), period.get("valueTexts", []), strict=True)
        if name.lower() != "annual"
    ]



def _format_price_context(
    data: dict[str, Any],
    metadata: dict[str, Any],
) -> str | None:
    """Format PSA prices using human-readable dimension labels."""
    columns = data.get("columns", [])

    dimension_columns = [
        column for column in columns
        if column.get("type") != "c"
    ]

    column_names = [
        column.get("text", column.get("code", "Value"))
        for column in dimension_columns
    ]

    # Resolve PSA commodity codes to their actual names.
    commodity_dimension = _get_dimension(metadata, "Commodity")
    commodity_codes = commodity_dimension.get("values", [])
    commodity_names = commodity_dimension.get("valueTexts", [])

    commodity_name_by_code = dict(
        zip(commodity_codes, commodity_names, strict=True)
    )

    records: list[dict[str, Any]] = []

    logger.debug("PSA columns: %r", columns)

    for row in data.get("data", []):
        keys = row.get("key", [])
        values = row.get("values", [])

        if not keys or not values or values[0] is None:
            continue

        if len(keys) != len(column_names):
            logger.warning(
                "PSA row key mismatch: keys=%d, columns=%d",
                len(keys),
                len(column_names),
            )
            continue

        records.append(
            dict(zip(column_names, keys, strict=True))
            | {"Price": values[0]}
        )

    if not records:
        return None

    latest_by_commodity: dict[str, dict[str, Any]] = {}

    for record in records:
        # Keep the original PSA code for reliable identification.
        commodity_code = str(record.get("Commodity", ""))
        current_record = latest_by_commodity.get(commodity_code)

        if (
            current_record is None
            or _record_period(record) > _record_period(current_record)
        ):
            latest_by_commodity[commodity_code] = record

    lines = [
        "PSA-reported Philippine retail prices:",
        "Commodity names below are resolved from official PSA metadata.",
    ]

    for commodity_code, record in latest_by_commodity.items():
        commodity_name = commodity_name_by_code.get(
            commodity_code,
            f"Unknown commodity (PSA code: {commodity_code})",
        )

        lines.append(
            f"- Commodity: {commodity_name} "
            f"(code: {commodity_code}); "
            f"Price: {record['Price']}; "
            f"Period: {record.get('Period')}, {record.get('Year')}; "
            f"Geolocation: {record.get('Geolocation')}"
        )

    return "\n".join(lines)


def _record_period(record: dict[str, Any]) -> tuple[int, int]:
    """Return a sortable year/month pair for a PSA result row."""
    try:
        year = int(record.get("Year", 0))
    except (TypeError, ValueError):
        year = 0

    month = _MONTH_ORDER.get(str(record.get("Period", "")).lower(), 0)
    return year, month


async def get_price_context_for_prompt(prompt: str) -> str | None:
    """Fetch and compact recent PSA prices for commodities named in a price question."""
    if not is_price_request(prompt):
        return None

    metadata = await fetch_psa_metadata()
    commodity_codes = find_commodity_codes(prompt, metadata)
    if not commodity_codes:
        return None

    data = await fetch_psa_data({
        "Geolocation": [PHILIPPINES_GEOLOCATION_CODE],
        "Commodity": commodity_codes,
        "Year": _get_recent_year_codes(metadata),
        "Period": _get_month_codes(metadata),
    })
    return _format_price_context(data, metadata)


@tool
async def get_psa_prices(prompt: str) -> str:
    """Fetch concise PSA-reported prices for commodities named in a price question.

    The prompt must contain the products to look up. Use when the user asks about
    PSA-reported prices; do not use it for non-price questions.
    """
    return (
        await get_price_context_for_prompt(prompt)
        or "No matching PSA commodity prices were found for that request."
    )
