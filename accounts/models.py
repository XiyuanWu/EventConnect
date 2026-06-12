from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField(max_length=120, blank=True, default="")
    bio = models.TextField(blank=True, default="")
    major = models.CharField(max_length=120, blank=True, default="")
    interests = models.CharField(max_length=255, blank=True, default="")
    google_sub = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self):
        return f"Profile({self.user})"
