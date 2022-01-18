import unittest
from decimal import Decimal
from unittest.mock import patch

from demo_api.price import amount_to_price

order_book_mock = {
    "timestamp": "1642474746",
    "microtimestamp": "1642474746109754",
    "bids": [["42254.87", "0.18325266"], ["42254.86", "3"], ["42253.73", "10"]],
    "asks": [["42272.58", "0.92458373"], ["42273.07", "3"], ["42279.86", "10"]],
}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if args[0]:
        return MockResponse(order_book_mock)

    return MockResponse(None)


class TestCasePrice(unittest.TestCase):
    @patch("requests.get", side_effect=mocked_requests_get)
    def test_amount_to_price(self, mock_response):
        test_cases = [
            {
                "expected_result_basic": {
                    "bid": Decimal("42254.87"),
                    "ask": Decimal("42272.58"),
                },
                "crypto_amount": Decimal("0.01"),
            },
            {
                "expected_result_basic": {
                    "bid": Decimal("42254.86"),
                    "ask": Decimal("42272.58"),
                },
                "crypto_amount": Decimal("0.2"),
            },
            {
                "expected_result_basic": {
                    "bid": Decimal("42254.86"),
                    "ask": Decimal("42273.07"),
                },
                "crypto_amount": Decimal("1"),
            },
            {
                "expected_result_basic": {
                    "bid": Decimal("42253.73"),
                    "ask": Decimal("42279.86"),
                },
                "crypto_amount": Decimal("7"),
            },
            {
                "expected_result_basic": {
                    "bid": Decimal("-1"),
                    "ask": Decimal("-1"),
                },
                "crypto_amount": Decimal("600"),
            },
        ]

        for test_case in test_cases:
            crypto_amount = test_case["crypto_amount"]
            if test_case["expected_result_basic"]["bid"] != Decimal("-1"):
                expected_result = {
                    "bid": test_case["expected_result_basic"]["bid"]
                    * crypto_amount,
                    "ask": test_case["expected_result_basic"]["ask"]
                    * crypto_amount,
                }
            else:
                expected_result = {
                    "bid": test_case["expected_result_basic"]["bid"],
                    "ask": test_case["expected_result_basic"]["ask"],
                }

            result = amount_to_price(
                crypto="btc", currency="eur", crypto_amount=crypto_amount
            )

            self.assertEqual(expected_result, result)
