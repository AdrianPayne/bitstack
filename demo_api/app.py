from decimal import Decimal
from fastapi import FastAPI

from demo_api.price import amount_to_price

app = FastAPI(title="Bitstack Demo API")


@app.get("/")
def root_get():
    return {"description": "Hello coder!"}


@app.get("/price/{crypto}/{currency}/{crypto_amount}")
def crypto_to_currency(crypto: str, currency: str, crypto_amount: Decimal):
    crypto_options = ['btc', 'eth', 'xrp']
    currency_options = ['usd', 'eur', 'gbp', 'bch', 'xlm']  # Only some crypto examples
    return amount_to_price(crypto, currency, crypto_amount)

