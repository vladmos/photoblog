# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

import views

urlpatterns = patterns('',
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/admin/login/'}, name='logout'),
    url(r'^$', views.index, name='index'),
)

