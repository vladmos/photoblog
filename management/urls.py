# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

import views
from forms import CustomAuthenticationForm

urlpatterns = patterns('',
    url(r'^login/$', login, {
        'template_name': 'login.html',
        'authentication_form': CustomAuthenticationForm,
    }, name='login'),
    url(r'^logout/$', logout, {'next_page': '/admin/login/'}, name='logout'),

    url(r'^$', views.index, name='index'),

    url(r'^settings/$', views.user_settings, name='settings'),
    url(r'^settings/save/$', views.change_settings, name='change_settings'),
    url(r'^settings/password/$', views.change_password, name='change_password'),

    url(r'^album/$', views.list_photoalbums, name='photoalbums'),
    url(r'^album/(?P<photoalbum_id>\d+)/$', views.view_photoalbum, name='photoalbum'),

    url(r'^article/$', views.list_articles, name='articles'),
    url(r'^article/new/$', views.view_article, name='new_article'),
    url(r'^article/(?P<article_id>\d+)/$', views.view_article, name='article'),
    url(r'^article/new/save/$', views.save_article, name='save_article'),
    url(r'^article/(?P<article_id>\d+)/save/$', views.save_article, name='save_article'),

    url(r'^ajax/album/(?P<photoalbum_id>\d+)/$', views.preview_photoalbum, name='preview_photoalbum'),
    url(r'^ajax/article/$', views.preview_article, name='preview_article'),

    url(r'^update_albums/$', views.update_albums, name='update_albums'),
)

