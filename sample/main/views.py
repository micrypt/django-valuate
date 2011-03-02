from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import Post
import settings

def home(request):
    posts = Post.objects.all()
    return render_to_response('home.html',
                              {'STATIC_ROOT':settings.STATIC_ROOT,
                               'posts':posts},
                              context_instance=RequestContext(request))
