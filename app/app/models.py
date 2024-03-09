import time
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Image and Thumbnail related libraries
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os, datetime, random, string
from django.utils import timezone
from . import common_variables


class Settings(models.Model):
    # key=SECTION::KEY
    key = models.CharField(primary_key=True, max_length=128)
    value = models.CharField(max_length=512)

    def get_section(self):
        return self.key.split("::")[0].split(":")[0]

    def get_key_name(self):
        return self.key.split("::")[0].split(":")[1]

    def get_icon(self):
        section = self.get_section()
        if section == "notif":
            return '<i class="fa-solid fa-bell" style="color: #74C0FC;"></i>'
        elif section == "app":
            return '<i class="fa-solid fa-gears" style="color: #74C0FC;"></i>'
        else:
            return ''

    def get_name(self):
        return self.key.split("::")[1]


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


class TelegramSubscribe(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_telegram_subscribers')


class UserProfile(models.Model):
    default_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscription_plan = models.CharField(max_length=64, default="free")
    activated = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)


class Token(models.Model):
    id = models.CharField(primary_key=True, max_length=common_variables.ONE_TIME_TOKEN_LENGTH)
    expiry = models.DateTimeField()
    used_id = models.UUIDField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits,
                                         k=common_variables.ONE_TIME_TOKEN_LENGTH))
        self.expiry = datetime.datetime.now() + common_variables.ONE_TIME_TOKEN_LENGTH
