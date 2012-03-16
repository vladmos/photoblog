from django.db import models
from django.contrib.auth.models import User

class PicasaAlbum(models.Model):
    user = models.ForeignKey(User, related_name='albums')
    name = models.CharField(max_length=255)
    picasa_id = models.CharField(max_length=20)
    is_public = models.BooleanField()

    class Meta:
        unique_together = ('picasa_id', 'user')


class PicasaPhoto(models.Model):
    album = models.ForeignKey('PicasaAlbum', related_name='photos')
    picasa_id = models.CharField(max_length=20)
    page_url = models.URLField()
    photo_url = models.URLField()
    thumbnail_url = models.URLField()
    description = models.TextField(null=True)

    class Meta:
        unique_together = ('picasa_id', 'album')
