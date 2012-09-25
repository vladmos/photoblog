from django.conf.urls.defaults import patterns, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^~/', include(admin.site.urls)),
    
    (r'^oauth/', include('personal.urls', namespace='personal')),
    (r'^admin/', include('management.urls', namespace='management')),
    (r'^', include('frontend.urls', namespace='frontend')),
)

urlpatterns += staticfiles_urlpatterns()