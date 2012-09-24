# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.blog, name='blog'),
    url(r'^~rss/$', views.rss, name='rss'),
    url(r'^(?P<article_slug>[\w\-]+)/$', views.article, name='article'),
)
