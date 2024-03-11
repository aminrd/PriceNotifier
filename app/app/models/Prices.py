import datetime
import time
from uuid import uuid4
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
        return self.low_value < self.base_value < self.high_value and self.low_value >= 0.0 and len(self.name) > 0


class Stock(models.Model, ChangeLogBase):
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
