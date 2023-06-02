from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    openai_api_key = models.CharField(max_length=300, null=True, blank=True, default='')
