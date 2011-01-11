from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from main.models import Post
import settings

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html',
                              {'STATIC_ROOT':settings.STATIC_ROOT, 'posts':posts})
