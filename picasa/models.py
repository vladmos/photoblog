from django.db import models
from django.contrib.auth.models import User

class PicasaAlbum(models.Model):
    user = models.ForeignKey(User, related_name='albums')
    name = models.CharField(max_length=255)
    picasa_id = models.CharField(max_length=20, unique=True)
    is_public = models.BooleanField()