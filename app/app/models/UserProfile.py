from django.db import models
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class UserProfile(models.Model):
    default_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscription_plan = models.CharField(max_length=64, default="free")
    activated = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)


def get_users(top: int, skip: int = 0):
    return User.objects.all()[skip:top]


async def get_users_async(top: int, skip: int = 0):
    await sync_to_async(get_users, thread_sensitive=True)(top, skip)
