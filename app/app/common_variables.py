from datetime import timedelta

PRICE_TYPES = [
    "url",
    "stock",
    "ctrypto"
]


class Result:
    success = False
    item = None
    message = None


ONE_TIME_TOKEN_LENGTH = 32
TOKEN_LIFETIME = timedelta(1)
