from django.db import models
from django.forms import ModelForm

class Post(models.Model):    
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title
