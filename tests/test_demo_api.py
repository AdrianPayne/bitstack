from datetime import timedelta

import hypothesis
import requests
import unittest
import schemathesis
from starlette.testclient import TestClient

from demo_api.app import app

schemathesis.fixups.install(["fast_api"])
schema = schemathesis.from_asgi("/openapi.json", app)

client = TestClient(app)


@schema.parametrize()
@hypothesis.settings(
    suppress_health_check=[
        hypothesis.HealthCheck.filter_too_much,
        hypothesis.HealthCheck.too_slow,
    ]
)
def test_fuzz(case):
    response: requests.Response = case.call(
        session=client,
    )
    assert response.elapsed < timedelta(milliseconds=500)
    case.validate_response(response)


# /price
class TestCasePrice(unittest.TestCase):
    def test_price_ok(self):
        crypto = 'btc'
        currency = 'usd'
        crypto_amount = 2
        response = client.get(f"/price/{crypto}/{currency}/{crypto_amount}")
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json()['bid'] and response.json()['ask'])

    def test_price_ko(self):
        crypto = ''
        currency = ''
        crypto_amount = 0
        response = client.get(f"/price/{crypto}/{currency}/{crypto_amount}")
        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Not Found'}, response.json())
