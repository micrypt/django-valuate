from django.conf.urls.defaults import patterns, url
import django.views.generic as gen_views
from main.models import * 
urlpatterns = patterns('',
    url(r'^post/$', 'valuate.views.submit', name = 'valuate-submit'),    
    url(r'^form/$', 'valuate.views.render_form', name = 'valuate-form'),
)
