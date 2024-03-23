import pytz
import datetime
import random
import string
from django.db import models
from django.contrib.auth.models import User
from .. import common_variables


def now():
    return datetime.datetime.now(tz=pytz.timezone('UTC'))


class Token(models.Model):
    id = models.CharField(primary_key=True, max_length=common_variables.ONE_TIME_TOKEN_LENGTH)
    expiry = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_token")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.id is None or len(self.id) < 1:
            self.id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits,
                                             k=common_variables.ONE_TIME_TOKEN_LENGTH))
            self.expiry = now() + common_variables.TOKEN_LIFETIME

    def is_expired(self):
        return self.expiry <= now()

    def expiry_seconds(self):
        if self.expiry > now():
            return (self.expiry - now()).total_seconds()
        return 0


def get_or_create_token_for_user(user: User) -> Token:
    existing_tokens = list(user.user_token.all().order_by('-expiry'))

    # remove older tokens
    while len(existing_tokens) > 1 or (len(existing_tokens) == 1 and existing_tokens[0].is_expired()):
        last_token = existing_tokens.pop()
        last_token.delete()

    if len(existing_tokens) > 0:
        return existing_tokens[0]

    token = Token(user=user)
    token.save()
    return token
