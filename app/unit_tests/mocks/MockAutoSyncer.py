import time
from app.models.Prices import ChangeLogBase


class MockAutoSyncer:
    def __init__(self, price_adjust=1.0):
        self.price_adjust = price_adjust

    async def update_async(self, changelog: ChangeLogBase) -> ChangeLogBase:
        changelog.last_value *= self.price_adjust
        changelog.last_check_timestamp = time.time()
        return changelog
