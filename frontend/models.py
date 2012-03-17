import datetime

from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    user = models.ForeignKey(User, related_name='articles')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    raw_text = models.TextField()
    compiled_text = models.TextField()
    created = models.DateField(default=datetime.datetime.now)

    def __unicode__(self):
        return u'%s: %s' % (
            self.user.username,
            self.name,1
        )

    class Meta:
        unique_together = ('slug', 'user')
        ordering = ['created']
