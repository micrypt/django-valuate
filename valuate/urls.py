from django.conf.urls.defaults import patterns, url
import django.views.generic as gen_views

urlpatterns = patterns('',
    url(r'^submit/$', 'valuate.views.submit', name = 'valuate-submit'),    
)
