from django.conf.urls.defaults import patterns, url
import django.views.generic as gen_views
from main.models import * 
urlpatterns = patterns('',
    url(r'^post/rating/$', 'valuate.views.post_rating', name = 'valuate-rating'),
    url(r'^post/like/$', 'valuate.views.post_like', name = 'valuate-like'),
    url(r'^form/$', 'valuate.views.render_form', name = 'valuate-form'),
)
