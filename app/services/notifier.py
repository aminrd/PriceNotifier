from django.contrib.auth.models import User
from app.models.Prices import get_user_changelogs_async
from app.models.UserProfile import get_users_async
from app.models.Subscribers import UserRepository
from dispatcher import Dispatcher
from auto_syncer import AutoSyncer


class Notifier:
    def __init__(self, owner: User, auto_syncer: AutoSyncer):
        self.owner = owner
        self.stocks = None
        self.subscribers = []
        self.auto_syncer = auto_syncer
        self.user_repository = UserRepository(owner)

    async def get_price_updates(self):
        # Get all subscribers
        self.subscribers = await self.user_repository.get_user_subscribers_async()

        # Get all price changelog objects
        changelogs = await get_user_changelogs_async(self.owner)

        for changelog in changelogs:
            update_changelog = await self.auto_syncer.update_async(changelog=changelog)
            if update_changelog.should_notify():
                yield update_changelog


class Notifiers:
    def __init__(self, dispatcher: Dispatcher = None, auto_syncer: AutoSyncer = None, top: int = 100, skip: int = 0):
        if dispatcher is None:
            raise Exception("Dispatchers are not provided")

        if auto_syncer is None:
            raise Exception("Auto syncer cannot be empty!")

        self.dispatcher = dispatcher
        self.top = top
        self.skip = skip
        self.auto_syncer = auto_syncer

    async def start(self):
        users = await get_users_async(self.top, self.skip)
        notifiers = [Notifier(user, self.auto_syncer) for user in users]

        for notifier in notifiers:
            async for price_update in notifier.get_price_updates():
                await self.dispatcher.dispatch_msg_to_user_async(price_update, notifier.subscribers)
