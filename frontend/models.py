# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from utils import compile_article

class Article(models.Model):
    user = models.ForeignKey(User, related_name='articles')
    name = models.CharField(max_length=255, verbose_name=_(u'Header'))
    slug = models.SlugField(max_length=100, verbose_name=_(u'Name in URL'))
    raw_text = models.TextField(verbose_name=_(u'Raw text'))
    compiled_text = models.TextField()
    year = models.IntegerField()
    event_beginning = models.DateField(verbose_name=_(u'Event started'))
    event_end = models.DateField(verbose_name=_(u'Event finished'))
    is_published = models.BooleanField(verbose_name=_(u'Published'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.compiled_text = compile_article(self.user, self.raw_text)
        self.year = self.event_beginning.year
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('frontend:article', kwargs={'year': self.event_beginning.year, 'slug': self.slug})

    def event_date_human(self):
        if self.event_beginning == self.event_end:
            return self.event_beginning.strftime('%d.%m.%Y')
        return u'%s — %s' % (
            self.event_beginning.strftime('%d.%m.%Y'),
            self.event_end.strftime('%d.%m.%Y'),
        )

    def __unicode__(self):
        return u'%s: %s' % (
            self.user.username,
            self.name,
        )

    class Meta:
        unique_together = ('slug', 'user', 'year')
        ordering = ['event_end']
