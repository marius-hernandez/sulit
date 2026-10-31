import re
from typing import Any

from app.services.prices.psa_client import psa_client
from app.services.prices.registry import MARKET_DATASETS, MarketDataset

_NOISE = {"fresh", "edible", "loose", "dressed", "whole", "kg", "pc", "price", "prices", "market", "how", "much", "cost", "what", "are", "the", "of"}
_SPLIT = re.compile(r"\s*(?:,|/|&|\band\b)\s*", re.IGNORECASE)


def _words(value: str) -> set[str]:
    words = re.findall(r"[a-z]+", value.lower())
    return {word[:-1] if len(word) > 3 and word.endswith("s") else word for word in words if word not in _NOISE}


def _dimension(metadata: dict[str, Any], code: str) -> dict[str, Any]:
    for variable in metadata.get("variables", []):
        if variable.get("code") == code:
            return variable
    raise ValueError(f"PSA metadata is missing the '{code}' dimension.")


def _candidate_datasets(prompt: str) -> list[MarketDataset]:
    prompt_words = _words(prompt)
    return [
        dataset for dataset in MARKET_DATASETS
        if any(_words(alias) & prompt_words for alias in dataset.aliases)
    ]


def _match_codes(prompt: str, metadata: dict[str, Any]) -> list[str]:
    commodity = _dimension(metadata, "Commodity")
    codes, names = commodity.get("values", []), commodity.get("valueTexts", [])
    if len(codes) != len(names):
        raise ValueError("PSA Commodity metadata has mismatched values and valueTexts.")

    matched: list[str] = []
    requested_terms = [term for term in _SPLIT.split(prompt) if _words(term)]
    for term in requested_terms:
        term_words = _words(term)
        term_matches: list[tuple[str, int]] = []
        for code, name in zip(codes, names, strict=True):
            catalog_words = _words(name)
            if "egg" in catalog_words and "egg" not in term_words:
                continue
            score = len(catalog_words & term_words)
            if score:
                term_matches.append((code, score))
        if term_matches:
            highest = max(score for _, score in term_matches)
            for code, score in term_matches:
                if score == highest and code not in matched:
                    matched.append(code)
    return matched


async def resolve_commodity_datasets(
    prompt: str,
) -> list[tuple[MarketDataset, dict[str, Any], list[str]]]:
    resolved = []
    for dataset in _candidate_datasets(prompt):
        metadata = await psa_client.get_metadata(dataset)
        codes = _match_codes(prompt, metadata)
        if codes:
            resolved.append((dataset, metadata, codes))
    return resolved


def recent_year_codes(metadata: dict[str, Any], count: int = 2) -> list[str]:
    values = _dimension(metadata, "Year").get("values", [])
    if not values:
        raise ValueError("PSA metadata has no Year values.")
    return values[-count:]


def month_codes(metadata: dict[str, Any]) -> list[str]:
    period = _dimension(metadata, "Period")
    return [
        code for code, label in zip(period.get("values", []), period.get("valueTexts", []), strict=True)
        if str(label).strip().lower() != "annual"
    ]
