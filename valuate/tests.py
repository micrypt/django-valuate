"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.test.client import Client
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType as CT
from main.models import *
from valuate.models import *
#from valuate.forms import *

class Dummy(object):
    pass

request = Dummy()
request.user = Dummy()
request.user.is_authenticated = False
request.COOKIES = {'sessionid':'testid'}
request.META = {'REMOTE_ADDR':'127.0.0.1'}
    
class ModelTests(TestCase):
    def test_create(self):
        post = Post.objects.create(title = 'Test Post')
        field_dict = {
                      'content_type':CT.objects.get_for_model(post),
                      'object_pk': post.pk,
                      'value':4,
                      }
        valuation = Valuation(**field_dict)
        valuation.save(request=request)        
        print valuation, valuation.session, valuation.ip_address

__test__ = {
}

