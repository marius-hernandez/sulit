import unittest

from app.services.prices.formatter import format_price_context
from app.services.prices.resolver import _match_codes, month_codes, recent_year_codes


METADATA = {
    "variables": [
        {"code": "Commodity", "values": ["0", "1", "2"], "valueTexts": [
            "FRESH CHICKEN, BREAST, 1 KG", "FRESH CHICKEN, LEGS, 1 KG",
            "FRESH EGG, CHICKEN, MEDIUM, 1 PC",
        ]},
        {"code": "Geolocation", "values": ["000000000"], "valueTexts": ["Philippines"]},
        {"code": "Year", "values": ["2025", "2026"], "valueTexts": ["2025", "2026"]},
        {"code": "Period", "values": ["01", "02"], "valueTexts": ["June", "July"]},
    ]
}


class PsaPricesTests(unittest.TestCase):
    def test_matches_specific_commodity(self):
        self.assertEqual(_match_codes("chicken breasts", METADATA), ["0"])

    def test_matches_all_chicken_products_for_broad_request(self):
        self.assertEqual(_match_codes("chicken", METADATA), ["0", "1"])

    def test_year_and_month_codes_come_from_metadata(self):
        self.assertEqual(recent_year_codes(METADATA), ["2025", "2026"])
        self.assertEqual(month_codes(METADATA), ["01", "02"])

    def test_formats_latest_price_using_metadata_labels(self):
        result = format_price_context("poultry", {
            "columns": [
                {"code": "Geolocation", "type": "d"},
                {"code": "Commodity", "type": "d"},
                {"code": "Year", "type": "d"},
                {"code": "Period", "type": "d"},
                {"code": "Value", "type": "c"},
            ],
            "data": [
                {"key": ["000000000", "0", "2025", "01"], "values": [210.0]},
                {"key": ["000000000", "0", "2026", "02"], "values": [220.0]},
            ],
        }, METADATA)
        self.assertIn("FRESH CHICKEN, BREAST, 1 KG", result)
        self.assertIn("220.0", result)
        self.assertNotIn("210.0", result)


if __name__ == "__main__":
    unittest.main()
