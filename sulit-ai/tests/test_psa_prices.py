import unittest

from app.tools.psa_prices import _format_price_context, find_commodity_codes


METADATA = {
    "variables": [
        {
            "code": "Commodity",
            "values": ["0", "1", "2"],
            "valueTexts": [
                "FRESH CHICKEN, BREAST, 1 KG",
                "FRESH CHICKEN, LEGS, 1 KG",
                "FRESH EGG, CHICKEN, MEDIUM, 1 PC",
            ],
        }
    ]
}


class PsaPricesTests(unittest.TestCase):
    def test_finds_most_specific_commodity_in_prompt(self) -> None:
        result = find_commodity_codes("What is the price of chicken breasts?", METADATA)

        self.assertEqual(result, ["0"])

    def test_finds_all_commodities_in_a_multi_good_prompt(self) -> None:
        result = find_commodity_codes("What are the prices of chicken and eggs?", METADATA)

        self.assertEqual(result, ["0", "1", "2"])

    def test_finds_all_equally_specific_commodities(self) -> None:
        result = find_commodity_codes("What are the chicken prices?", METADATA)

        self.assertEqual(result, ["0", "1"])

    def test_formats_only_available_price_records(self) -> None:
        result = _format_price_context({
            "columns": [
                {"text": "Geolocation"},
                {"text": "Commodity"},
                {"text": "Year"},
                {"text": "Period"},
            ],
            "data": [
                {
                    "key": ["PHILIPPINES", "FRESH CHICKEN, BREAST, 1 KG", "2025", "December"],
                    "values": [210.0],
                },
                {
                    "key": ["PHILIPPINES", "FRESH CHICKEN, BREAST, 1 KG", "2026", "June"],
                    "values": [215.0],
                },
                {
                    "key": ["PHILIPPINES", "FRESH CHICKEN, BREAST, 1 KG", "2026", "July"],
                    "values": [220.0],
                },
                {
                    "key": ["PHILIPPINES", "FRESH CHICKEN, LEGS, 1 KG", "2026", "July"],
                    "values": [None],
                },
            ],
        })

        self.assertIsNotNone(result)
        self.assertIn("220.0 (July, 2026; PHILIPPINES)", result)
        self.assertNotIn("215.0", result)
        self.assertNotIn("210.0", result)


if __name__ == "__main__":
    unittest.main()