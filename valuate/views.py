from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from valuate.models import Rating, get_object_ctype_pk
from valuate.forms import RatingForm, LikeForm
from main.models import *

def render_form(request):    
    post = Post.objects.get_or_create(title = 'Test')[0]
    content_type, object_pk = get_object_ctype_pk(post)
    form = RatingForm(initial={'content_type':content_type, 'object_pk':object_pk}, auto_id=False)
    form_template_string = render_to_string('valuate/form.html', {'form': form}, context_instance = RequestContext(request))
    form_html = '<form method="post" action="%s">\n%s' %(reverse('valuate-rating'), form_template_string)
    return HttpResponse(form_html)

@csrf_protect
@require_POST
def post_rating(request):    
    form = RatingForm(request.POST)
    if form.is_valid():
        rating = form.save(commit=False)        
        if request.user.is_authenticated:
            rating.user = request.user 
        rating.session = request.COOKIES.get('sessionid', '')
        rating.save()
        return HttpResponse(form, mimetype = "text/plain")    
    return HttpResponseRedirect(request.REQUEST.get('next', request.META['HTTP_REFERER']))
    
@csrf_protect
@require_POST
def post_like(request):    
    form = LikeForm(request.POST)
    if form.is_valid():
        like = form.save(commit=False)
        if request.user.is_authenticated:
            like.user = request.user 
        like.session = request.COOKIES.get('sessionid', '')
        like.save()
        return HttpResponse(form, mimetype = "text/plain")    
    return HttpResponseRedirect(request.REQUEST.get('next', request.META['HTTP_REFERER']))
    
