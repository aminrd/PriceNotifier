import uuid
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Image and Thumbnail related libraries
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os, datetime, random, string
from django.utils import timezone
from .common_variables import *

class Settings(models.Model):
    section = models.CharField(default='section', max_length=16)
    key = models.CharField(max_length=512)
    value = models.CharField(max_length=512)

class Stock(models.Model):
    pass

class Other(models.Model):
    pass