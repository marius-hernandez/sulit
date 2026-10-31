import logging
from typing import Any

from app.services.prices.resolver import _dimension

logger = logging.getLogger(__name__)

_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def _period_key(record: dict[str, str]) -> tuple[int, int]:
    try:
        year = int(record.get("Year", "0"))
    except (TypeError, ValueError):
        year = 0
    return year, _MONTHS.get(record.get("Period", "").lower(), 0)


def format_price_context(
    dataset_name: str,
    data: dict[str, Any],
    metadata: dict[str, Any],
) -> str | None:
    """Translate PXWeb category codes to labels and keep the latest row per commodity."""
    columns = [column for column in data.get("columns", []) if column.get("type") != "c"]
    dimension_codes = [column.get("code") for column in columns]
    if not dimension_codes or any(not code for code in dimension_codes):
        logger.warning("PXWeb response for %s has missing dimension column codes.", dataset_name)
        return None

    label_maps: dict[str, dict[str, str]] = {}
    for code in dimension_codes:
        dimension = _dimension(metadata, code)
        values = dimension.get("values", [])
        labels = dimension.get("valueTexts", [])
        if len(values) != len(labels):
            raise ValueError(f"PSA metadata dimension '{code}' has mismatched labels.")
        label_maps[code] = dict(zip(values, labels, strict=True))

    latest: dict[str, tuple[tuple[int, int], dict[str, str], Any]] = {}
    for row in data.get("data", []):
        keys, values = row.get("key", []), row.get("values", [])
        if len(keys) != len(dimension_codes) or not values or values[0] is None:
            continue
        record = {
            code: label_maps[code].get(key, key)
            for code, key in zip(dimension_codes, keys, strict=True)
        }
        commodity_code = keys[dimension_codes.index("Commodity")] if "Commodity" in dimension_codes else ""
        commodity_labels = label_maps.get("Commodity", {})
        commodity_name = commodity_labels.get(commodity_code, commodity_code)
        period = _period_key(record)
        previous = latest.get(commodity_code)
        if previous is None or period > previous[0]:
            latest[commodity_code] = (period, record | {"Commodity": commodity_name}, values[0])

    if not latest:
        return None

    lines = [f"PSA-reported Philippine retail prices ({dataset_name}):"]
    for code, (_, record, price) in sorted(latest.items()):
        lines.append(
            f"- {record.get('Commodity', 'Unknown commodity')} (PSA code: {code}): "
            f"{price}; {record.get('Period', 'unknown period')} {record.get('Year', '')}; "
            f"{record.get('Geolocation', 'Philippines')}"
        )
    return "\n".join(lines)
