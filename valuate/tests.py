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
from valuate.forms import *

class Dummy(object):
    pass

request = Dummy()
request.user = Dummy()
request.user.is_authenticated = False
request.COOKIES = {'sessionid':'testid'}
request.META = {'REMOTE_ADDR':'localhost'}

    
class FormTests:    
    def test_validation(self):
        post = Post.objects.create(title = 'Test Post')
        f = self.Form({'content_type':CT.objects.get_for_model(post).id, 'object_pk': post.pk, 'rating':4})        
        self.assertEqual(f.is_valid(), True)
        return f

    def test_save(self):
        obj = self.test_validation().save(request)        
        print '\n', obj
        return obj

class RatingFormTests(TestCase, FormTests):
    Model = Rating
    Form = RatingForm    

class LikeButtonFormTests(TestCase, FormTests):
    Model = Like
    Form = LikeForm
    
__test__ = {
##"models": """
##>>> from django.contrib.contenttypes.models import ContentType as CT
##>>> from main.models import *
##>>> from valuate.models import *
##>>> import settings
##>>> post = Post.objects.create(title="Test")
##>>> Rating.objects.create_for_object(post, rating = 3, site_id = settings.SITE_ID)
##<Rating: Test(post), Rating: Average>
##>>> Rating.objects.create_for_object(post, rating = 5, site_id = settings.SITE_ID)
##<Rating: Test(post), Rating: Excelent>
##>>> Rating.objects.get_for_object(post)
##[<Rating: Test(post), Rating: Average>, <Rating: Test(post), Rating: Excelent>]
##>>> LikeButton.objects.create_for_object(post, site_id = settings.SITE_ID)
##<LikeButton: Test(post), LikeButton>
##>>> LikeButton.objects.create_for_object(post, site_id = settings.SITE_ID)
##<LikeButton: Test(post), LikeButton>
##>>> LikeButton.objects.get_count_for_object(post)
##2
##""",
}

