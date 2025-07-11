from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('creator', 'Creator'),
        ('viewer', 'Viewer'),
    )
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.user_type})"

class CreatorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='creator_profile')
    restaurant_name = models.CharField(max_length=255, blank=True, null=True)

class ViewerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='viewer_profile')
    address = models.TextField(blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True)