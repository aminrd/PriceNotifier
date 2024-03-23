from django.contrib.auth.models import User
from app.models.Prices import get_user_changelogs_async
from app.models.UserProfile import get_users_async
from app.models.Subscribers import get_user_subscribers_async
from app.utility.stock import sync_stock_async
from dispatcher import Dispatcher


class Notifier:
    def __init__(self, owner: User):
        self.owner = owner
        self.stocks = None
        self.subscribers = []

    async def get_price_updates(self):
        # Get all subscribers
        self.subscribers = await get_user_subscribers_async(self.owner)

        # Get all price changelog objects
        changelogs = await get_user_changelogs_async(self.owner)

        for changelog in changelogs:
            update_changelog = None
            if changelog.price_type == 'stock':
                update_changelog = await sync_stock_async(changelog)
            else:
                continue

            if update_changelog.should_notify():
                yield update_changelog


class Notifiers:
    def __init__(self, dispatcher: Dispatcher = None, top: int = 100, skip: int = 0):
        if dispatcher is None:
            raise Exception("Dispatchers are not provided")

        self.dispatcher = dispatcher
        self.top = top
        self.skip = skip

    async def start(self):
        users = await get_users_async(self.top, self.skip)
        notifiers = [Notifier(user) for user in users]

        for notifier in notifiers:
            async for price_update in notifier.get_price_updates():
                await self.dispatcher.dispatch_msg_to_user_async(price_update, notifier.subscribers)
