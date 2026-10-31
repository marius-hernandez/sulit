import asyncio
from typing import Any, Literal

import httpx

from app.services.prices.registry import MarketDataset

ResponseFormat = Literal["json", "csv", "json-stat", "json-stat2", "px"]
_TIMEOUT = httpx.Timeout(30.0, connect=10.0)
_METADATA_CACHE: dict[str, dict[str, Any]] = {}
_METADATA_LOCKS: dict[str, asyncio.Lock] = {}


def _metadata_lock(url: str) -> asyncio.Lock:
    # Called on the active event loop; one lock per table URL.
    return _METADATA_LOCKS.setdefault(url, asyncio.Lock())


class PsaClient:
    """Small async client for PSA PXWeb tables."""

    async def get_metadata(self, dataset: MarketDataset) -> dict[str, Any]:
        cached = _METADATA_CACHE.get(dataset.url)
        if cached is not None:
            return cached

        async with _metadata_lock(dataset.url):
            cached = _METADATA_CACHE.get(dataset.url)
            if cached is not None:
                return cached

            async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
                response = await client.get(dataset.url)
                response.raise_for_status()
                metadata = response.json()

            if not isinstance(metadata, dict) or not isinstance(metadata.get("variables"), list):
                raise ValueError(f"Invalid PXWeb metadata for dataset '{dataset.key}'.")
            _METADATA_CACHE[dataset.url] = metadata
            return metadata

    async def fetch_data(
        self,
        dataset: MarketDataset,
        selections: dict[str, list[str]],
        response_format: ResponseFormat = "json-stat",
    ) -> dict[str, Any]:
        if not selections:
            raise ValueError("At least one PXWeb dimension selection is required.")

        query = []
        for dimension, values in selections.items():
            if not values:
                raise ValueError(f"No values provided for PXWeb dimension '{dimension}'.")
            query.append({
                "code": dimension,
                "selection": {"filter": "item", "values": values},
            })

        payload = {"query": query, "response": {"format": response_format}}
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            response = await client.post(dataset.url, json=payload)
            response.raise_for_status()
            result = response.json()

        if not isinstance(result, dict):
            raise ValueError(f"Invalid PXWeb response for dataset '{dataset.key}'.")
        return result


psa_client = PsaClient()
