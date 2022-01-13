from datetime import timedelta

import hypothesis
import requests
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


def test_arbitrary_zero_case():
    response = client.get("/price/0/0/0.0")
    assert response.status_code == 200
