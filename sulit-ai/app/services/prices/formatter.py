from dataclasses import dataclass

@dataclass(frozen=True)
class MarketDataset:
    name: str
    url: str

_PSA_BASE_URL="https://openstat.psa.gov.ph/PXWeb/api/v1/en/"

MARKET_DATASETS: dict[str, MarketDataset] = {
    "cereals": MarketDataset(
        name="cereals",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN01.px"
    ),
    "root-crops": MarketDataset(
        name="root-crops",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN02.px"
    ),
    "legumes": MarketDataset(
        name="legumes",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN03.px"
    ),
    "condiments": MarketDataset(
        name="condiments",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN04.px"
    ),
    "fruit-vegetables": MarketDataset(
        name="fruit-vegetables",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN05.px"
    ),
    "leafy-vegetables": MarketDataset(
        name="leafy-vegetables",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN06.px"
    ),
    "fruits": MarketDataset(
        name="fruits",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN07.px"
    ),
    "commercial-crops": MarketDataset(
        name="commercial-crops",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN08.px"
    ),
    "livestock": MarketDataset(
        name="livestock",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN09.px"
    ),
    "poultry": MarketDataset(
        name="poultry",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN10.px"
    ),
    "fish": MarketDataset(
        name="fish",
        url= _PSA_BASE_URL+ "DB/2M/2018NEW/0042M4ARN11.px"
    ),
}
