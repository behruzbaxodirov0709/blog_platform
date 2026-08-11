from django.db import models
from django.contrib.auth.models import AbstractUser 


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    social_links = models.JSONField(null=True, blank=True)
