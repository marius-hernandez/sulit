from dataclasses import dataclass

_BASE = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/2018NEW/"


@dataclass(frozen=True, slots=True)
class MarketDataset:
    key: str
    url: str
    aliases: tuple[str, ...]


# Dataset IDs follow the PSA table catalogue. Confirm dimensions/coverage from
# each table's metadata; never infer commodity codes from list positions.
MARKET_DATASETS: tuple[MarketDataset, ...] = (
    MarketDataset("cereals", _BASE + "0042M4ARN01.px", ("rice", "corn", "cereal")),
    MarketDataset("root-crops", _BASE + "0042M4ARN02.px", ("potato", "sweet potato", "cassava", "root crop")),
    MarketDataset("legumes", _BASE + "0042M4ARN03.px", ("beans", "munggo", "mung bean", "legume")),
    MarketDataset("condiments", _BASE + "0042M4ARN04.px", ("onion", "garlic", "ginger", "chili", "pepper", "condiment")),
    MarketDataset("fruit-vegetables", _BASE + "0042M4ARN05.px", ("tomato", "eggplant", "okra", "squash", "cucumber", "fruit vegetable")),
    MarketDataset("leafy-vegetables", _BASE + "0042M4ARN06.px", ("pechay", "cabbage", "lettuce", "kangkong", "spinach", "leafy vegetable")),
    MarketDataset("fruits", _BASE + "0042M4ARN07.px", ("banana", "mango", "apple", "orange", "papaya", "pineapple", "fruit")),
    MarketDataset("commercial-crops", _BASE + "0042M4ARN08.px", ("coffee", "cacao", "coconut", "commercial crop")),
    MarketDataset("livestock", _BASE + "0042M4ARN09.px", ("pork", "beef", "carabao", "livestock")),
    MarketDataset("poultry", _BASE + "0042M4ARN10.px", ("chicken", "egg", "duck", "quail", "poultry")),
    MarketDataset("fish", _BASE + "0042M4ARN11.px", ("fish", "bangus", "tilapia", "galunggong", "seafood", "shrimp")),
)

DATASETS_BY_KEY = {dataset.key: dataset for dataset in MARKET_DATASETS}
PHILIPPINES_GEOLOCATION_CODE = "000000000"
