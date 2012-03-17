# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^~(?P<username>\w+)/$', views.user_articles, name='user_articles'),
    url(r'^~(?P<username>\w+)/(?P<article_slug>[\w\-]+)/$', views.view_article, name='article'),
)

