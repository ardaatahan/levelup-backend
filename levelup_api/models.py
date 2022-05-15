from ssl import _PasswordType
from unittest.util import _MAX_LENGTH
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=50, null=False, unique=True)
    email = models.EmailField(max_length=60, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    phone = models.PhoneNumberField()
