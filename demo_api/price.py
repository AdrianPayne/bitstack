from decimal import Decimal

import requests


def amount_to_price(crypto: str, currency: str, crypto_amount: Decimal) -> dict:
    api_web = f"https://www.bitstamp.net/api/v2/order_book/{crypto}{currency}"
    response = requests.get(api_web).json()

    for bid in response["bids"]:
        if crypto_amount <= Decimal(bid[1]):
            bid = Decimal(bid[0]) * crypto_amount
            for ask in response["asks"]:
                if crypto_amount <= Decimal(ask[1]):
                    ask = Decimal(ask[0]) * crypto_amount
                    return {"bid": bid, "ask": ask}

    # Return -1 if quantity is too high
    return {"bid": Decimal(-1), "ask": Decimal(-1)}
