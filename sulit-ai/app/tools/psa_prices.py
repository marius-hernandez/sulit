
import httpx
from typing import Literal

from langchain_core.tools import tool

ResponseFormat = Literal["json", "csv", "json-stat", "json-stat2", "px"]

PSA_URL = (
    "https://openstat.psa.gov.ph/PXWeb/api/v1/en/"
    "DB/2M/2018NEW/0042M4ARN10.px"
)


def build_psa_query(
    selections: dict[str, list[str]],
    response_format: ResponseFormat = "json-stat",
) -> dict:
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
    selections: dict[str, list[str]],
) -> dict:
    """Fetch data from PSA. Not a LangChain tool."""
    payload = build_psa_query(selections)

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(PSA_URL, json=payload)
        response.raise_for_status()
        return response.json()


@tool
async def get_psa_prices() -> dict:
    """Fetch PSA-reported agricultural commodity price data.

    Use when the user asks about prices reported by PSA.
    The current query selects the configured years.
    """
    return await fetch_psa_data({
        "Year": ["6", "7", "8"],
    })
