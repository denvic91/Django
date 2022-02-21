from django.conf import settings
import pytz
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime

from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) < (self.activation_key_created + timedelta(hours=48)):
            return False
        return True



