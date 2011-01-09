"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

##class SimpleTest(TestCase):
##    def test_basic_addition(self):
##        """
##        Tests that 1 + 1 always equals 2.
##        """
##        self.failUnlessEqual(1 + 1, 2)

__test__ = {
"models_test": """
>>> from main.models import *
>>> from valuate.models import *
>>> from django.contrib.contenttypes.models import ContentType
>>> import settings
>>> post = Post.objects.create(title="Test")
>>> Rating.objects.create_for_object(post, rating = 3, site_id = settings.SITE_ID)
<Rating: Test(post), Rating: Average>
>>> Rating.objects.create_for_object(post, rating = 5, site_id = settings.SITE_ID)
<Rating: Test(post), Rating: Excelent>
>>> Rating.objects.get_for_object(post)
[<Rating: Test(post), Rating: Average>, <Rating: Test(post), Rating: Excelent>]
>>> Like.objects.create_for_object(post, site_id = settings.SITE_ID)
<Like: Test(post), Like>
>>> Like.objects.create_for_object(post, site_id = settings.SITE_ID)
<Like: Test(post), Like>
>>> Like.objects.get_count_for_object(post)
2
""",
}

