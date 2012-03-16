from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    oauth_token = models.CharField(max_length=255, null=True)


def create_profile(sender, created, instance, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()

post_save.connect(create_profile, sender=UserProfile)