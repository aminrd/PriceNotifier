from django.db import models
from django.contrib.auth.models import User


class TelegramSubscribe(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_telegram_subscribers')
