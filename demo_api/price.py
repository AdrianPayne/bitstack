from decimal import Decimal

import requests


def amount_to_price(crypto: str, currency: str, crypto_amount: Decimal) -> dict:
    api_web = f"https://www.bitstamp.net/api/v2/order_book/{crypto}{currency}"
    response = requests.get(api_web).json()

    bid = Decimal(response["bids"][0][0]) * crypto_amount
    ask = Decimal(response["asks"][0][0]) * crypto_amount

    return {"bid": bid, "ask": ask}
