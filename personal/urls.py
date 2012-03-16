# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^login/$', views.login, name='oauth_login'),
    url(r'^endpoint/$', views.endpoint, name='oauth_endpoint'),
)

