from django.test.client import Client
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpRequest
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType as CT
from main.models import *
from valuate.models import *
from valuate.forms import *

ANONYMOUS = False

##CREATING INITIAL OBJECTS
#Used get_or_create to prevent duplicaion as a serialized database dump is present

Post.objects.get_or_create(title='Test')[0]
post = Post.objects.get_or_create(title='Test Post')[0]

if ANONYMOUS:
    user = AnonymousUser()
else:
    user = User.objects.get_or_create(username='testuser', email='test@test.com')[0]

request = HttpRequest()
request.user = user
request.session = SessionStore()
request.session.save()
request.COOKIES['sessionid']=request.session.session_key

class ModelTests(TestCase):
    def test_create(self):        
        field_dict = {
                      'content_type':CT.objects.get_for_model(post),
                      'object_pk': post.pk,
                      'value':4,
                      }
        valuation = Valuation(**field_dict)
        valuation.save(request=request)
        self.failUnlessEqual(valuation.id, 1)        
        self.failUnlessEqual(valuation.user, request.user)        

class FormTests(TestCase):
    pass

__test__ = {
}
