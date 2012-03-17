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
    album_url = models.URLField()
    access_type = models.CharField(max_length=9, choices=ACCESS_TYPE_CHOICES)

    def __unicode__(self):
        return u'%s: %s' % (
            self.user.username,
            self.name,
        )

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

    def __unicode__(self):
        return u'%s: %s %s' % (
            self.album.user.username,
            self.album.name,
            self.picasa_id,
        )

    class Meta:
        unique_together = ('picasa_id', 'album')
