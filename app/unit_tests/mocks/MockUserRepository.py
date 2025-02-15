from django.contrib.auth.models import User
from app.models.Subscribers import TelegramSubscribe


class MockUserRepository:
    def __init__(self, user: User):
        self.user = user

    def get_user_subscribers(self):
        subscribers = []
        subscribers += [TelegramSubscribe(user=self.user) for _ in range(5)]
        return subscribers

    async def get_user_subscribers_async(self):
        return self.get_user_subscribers()
