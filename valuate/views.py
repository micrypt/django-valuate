from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType as CT
from valuate.forms import RatingForm, LikeForm
from main.models import *

Form = LikeForm
#A temporary view
def render_form(request):    
    post = Post.objects.get_or_create(title = 'Test')[0]    
    form = Form(obj = post, request = request)
    form_template_string = render_to_string('valuate/form.html', {'form': form}, context_instance = RequestContext(request))
    form_html = '<form method="post" action="%s">\n%s' %(reverse(form.target), form_template_string)
    return HttpResponse(form_html)

@csrf_protect
@require_POST
def post_rating(request):    
    form = RatingForm(request.POST)
    if form.is_valid():
        rating = form.save(request)
    return HttpResponse(request.REQUEST.get('next', request.META.get('HTTP_REFERER', '/')))    
    
@csrf_protect
@require_POST
def post_like(request):    
    form = LikeForm(request.POST)
    if form.is_valid():
        like = form.save(request)
    return HttpResponse(request.REQUEST.get('next', request.META.get('HTTP_REFERER', '/')))    
