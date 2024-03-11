from django.contrib import admin
from .models import *

admin.site.register(Stock)
admin.site.register(Other)
admin.site.register(Settings)
admin.site.register(Token)
admin.site.register(TelegramSubscribe)
admin.site.register(UserProfile)
