import datetime
import time
from typing import List
from uuid import uuid4
from asgiref.sync import sync_to_async
from django.db import models
from django.contrib.auth.models import User


def epoch_to_datetime(epoch: float) -> str:
    dt = datetime.datetime.fromtimestamp(epoch)
    return dt.astimezone().strftime('%Y-%m-%d %H:%M')


class ChangeLogBase:
    id = None
    name = None
    base_value = None
    high_value = None
    low_value = None
    last_value = None
    last_check_timestamp = None
    created_timestamp = None
    owner = None
    price_type = None
    notify = None

    def last_modified(self):
        return epoch_to_datetime(self.created_timestamp)

    def last_checked(self):
        return epoch_to_datetime(self.last_check_timestamp)

    def color(self):
        if self.base_value < self.last_value:
            return '#63E6BE'
        elif self.base_value > self.last_value:
            return '#d62e2e'
        else:
            return '#FFD43B'

    def change_icon(self):
        if self.base_value < self.last_value:
            return '<i class="fa-solid fa-arrow-trend-up" style="color: #63E6BE;"></i>'
        elif self.base_value > self.last_value:
            return '<i class="fa-solid fa-arrow-trend-down" style="color: #d62e2e;"></i>'
        else:
            return '<i class="fa-solid fa-equals" style="color: #FFD43B;"></i>'

    def is_valid(self):
        return self.high_value > self.base_value > self.low_value >= 0.0 and len(self.name) > 0

    def should_notify(self):
        return self.notify and (self.last_value >= self.high_value or self.last_value <= self.low_value)

    def get_raw_notification_msg(self):
        diff = self.base_value - self.last_value
        msg = f"""
            Your {self.price_type} {self.name} is now at {self.last_value}!
            ${abs(diff)} {'above' if diff > 0 else 'below'} the starting price at ${self.base_value}  
        """
        return msg

    def get_html_notification_msg(self):
        diff = self.base_value - self.last_value
        color = "red" if diff < 0 else "green"
        emoji = "⏫" if diff < 0 else "⏬"
        html = f"""
            Your {self.price_type} <b>{self.name}</b> is now at <strong style="color:{color};">{self.last_value}</string>!
            ${abs(diff)} {'above' if diff > 0 else 'below'} the starting price at <strong>${self.base_value}</strong> {emoji}  
        """
        return html


class Stock(models.Model, ChangeLogBase):
    price_type = "stock"
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_stocks")

    base_value = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    last_value = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    high_value = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    low_value = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)

    name = models.CharField(max_length=32)
    notify = models.BooleanField(default=True)
    last_check_timestamp = models.FloatField(default=time.time())
    created_timestamp = models.FloatField(default=time.time())

    code = models.CharField(max_length=16)

    def is_valid(self):
        return super().is_valid() and 0 < len(self.code) <= 16


class Other(models.Model, ChangeLogBase):
    price_type = "url track"
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_others")

    base_value = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    last_value = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    high_value = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    low_value = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)

    name = models.CharField(max_length=32)
    notify = models.BooleanField(default=True)
    last_check_timestamp = models.FloatField(default=time.time())
    created_timestamp = models.FloatField(default=time.time())

    url = models.CharField(max_length=1024)
    target_element = models.CharField(max_length=128)

    def url_short(self):
        return self.url[:50] + '....'


def get_user_changelogs(user: User) -> List[ChangeLogBase]:
    price_tracks = []
    price_tracks += list(user.user_stocks)
    price_tracks += list(user.user_others)
    return price_tracks


async def get_user_changelogs_async(user: User) -> List[ChangeLogBase]:
    stocks = await sync_to_async(get_user_changelogs, thread_sensitive=True)(user)
    return stocks
