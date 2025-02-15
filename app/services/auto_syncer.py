from app.models.Prices import ChangeLogBase, Stock, Other
from app.utility.stock import sync_stock_async


class AutoSyncer:
    def __init__(self):
        self.update_mapper = {
            Stock.price_type: sync_stock_async,
            Other.price_type: None
        }

    async def update_async(self, changelog: ChangeLogBase) -> ChangeLogBase:
        updater_function = self.update_mapper.get(changelog.price_type, None)
        if updater_function is None:
            return changelog

        updated_changelog = await updater_function(changelog)
        return updated_changelog
