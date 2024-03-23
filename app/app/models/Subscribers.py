from typing import List
from asgiref.sync import sync_to_async
from django.db import models
from django.contrib.auth.models import User


class Subscriber:
    user = None
    type = None


class TelegramSubscribe(models.Model, Subscriber):
    type = "telegram"
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_telegram_subscribers')


def get_user_subscribers(user: User) -> List[Subscriber]:
    subscribers = []
    subscribers += list(user.user_telegram_subscribers)
    return subscribers


async def get_user_subscribers_async(user: User) -> List[Subscriber]:
    subscribers = await sync_to_async(get_user_subscribers, thread_sensitive=True)(user)
    return subscribers
