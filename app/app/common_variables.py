APPLICATION_NAME = "PriceNotifier"

PRICE_TYPES = [
    "url",
    "stock",
    "ctrypto"
]

class Result:
    success = False
    item = None
    message = None