import datetime
import random
import string
from django.db import models
from .. import common_variables


class Token(models.Model):
    id = models.CharField(primary_key=True, max_length=common_variables.ONE_TIME_TOKEN_LENGTH)
    expiry = models.DateTimeField()
    used_id = models.UUIDField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits,
                                         k=common_variables.ONE_TIME_TOKEN_LENGTH))
        self.expiry = datetime.datetime.now() + common_variables.ONE_TIME_TOKEN_LENGTH
