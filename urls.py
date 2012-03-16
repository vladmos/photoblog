from django.conf.urls.defaults import patterns, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    
    (r'^oauth/', include('personal.urls', namespace='personal')),
    (r'^~/', include('management.urls', namespace='management')),
)
