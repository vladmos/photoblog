from django.db import models
from django.contrib.auth.models import User

ACCESS_TYPE_CHOICES = (
    ('public', u'Public'),
    ('private', u'Limited'),
    ('protected', u'Protected'),
)

class PicasaAlbum(models.Model):
    user = models.ForeignKey(User, related_name='albums')
    name = models.CharField(max_length=255)
    picasa_id = models.CharField(max_length=20)
    is_public = models.BooleanField()
    album_url = models.URLField()
    access_type = models.CharField(max_length=9, choices=ACCESS_TYPE_CHOICES)

    class Meta:
        unique_together = ('picasa_id', 'user')


class PicasaPhoto(models.Model):
    album = models.ForeignKey('PicasaAlbum', related_name='photos')
    picasa_id = models.CharField(max_length=20)
    page_url = models.URLField()
    photo_url = models.URLField()
    thumbnail_url = models.URLField()
    description = models.TextField(null=True)
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        unique_together = ('picasa_id', 'album')
