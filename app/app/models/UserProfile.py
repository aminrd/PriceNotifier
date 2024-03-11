from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    default_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscription_plan = models.CharField(max_length=64, default="free")
    activated = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
