from django.db import models
from django.contrib.auth.models import User

from utils import compile_article

class Article(models.Model):
    user = models.ForeignKey(User, related_name='articles')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    raw_text = models.TextField()
    compiled_text = models.TextField()
    event_beginning = models.DateField(verbose_name=u'Event started')
    event_end = models.DateField(verbose_name=u'Event finished')
    is_published = models.BooleanField(verbose_name=u'Published')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.compiled_text = compile_article(self.user, self.raw_text)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s: %s' % (
            self.user.username,
            self.name,
        )

    class Meta:
        unique_together = ('slug', 'user')
        ordering = ['event_end']
