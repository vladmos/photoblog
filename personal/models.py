from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils import HostnameValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    is_valid_token = models.BooleanField(default=False)
    oauth_token = models.CharField(max_length=255, null=True)

    custom_hostname = models.CharField(max_length=50, validators=[HostnameValidator()], blank=True)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()
