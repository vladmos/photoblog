# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>\w+)/$', views.blog, name='blog'),
    url(r'^(?P<username>\w+)/~rss/$', views.rss, name='rss'),
    url(r'^(?P<username>\w+)/(?P<article_slug>[\w\-]+)/$', views.view_article, name='article'),
)

