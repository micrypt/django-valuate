from django.test.client import Client
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpRequest
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType as CT
from main.models import *
from valuate.models import *
#from valuate.forms import *

ANONYMOUS = False

##CREATING INITIAL OBJECTS
#Used get_or_create to prevent duplicaion as a serialized database dump is present

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
    def setUp(self):
        Post.objects.get_or_create(title='Test')[0]
        self.post = Post.objects.get_or_create(title='Test Post')[0]
        vtype = ValuationType.objects.create(title='default')
        self.choice_1 = ValuationChoice.objects.create(name='low',
                                                       value=1,
                                                       vtype=vtype)
        self.choice_2 = ValuationChoice.objects.create(name='medium',
                                                       value=2,
                                                       vtype=vtype)
        self.choice_3 = ValuationChoice.objects.create(name='high',
                                                       value=3,
                                                       vtype=vtype)
        like_type = ValuationType.objects.create(title='like-dislike')
        self.like = ValuationChoice.objects.create(name='like',
                                                       value=1,
                                                       vtype=vtype)
        self.dislike = ValuationChoice.objects.create(name='dislike',
                                                       value=0,
                                                       vtype=vtype)        
        
    def test_create(self):        
        field_dict = {
                      'content_type':CT.objects.get_for_model(self.post),
                      'object_pk': self.post.pk,
                      'choice':self.choice_2,
                      }
        valuation = Valuation(**field_dict)
        valuation.save(request=request)
        self.failUnlessEqual(valuation.id, 1)        
        self.failUnlessEqual(valuation.user, request.user)        

class FormTests(TestCase):
    pass

__test__ = {
}
