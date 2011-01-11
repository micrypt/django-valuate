from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType as CT
from valuate.forms import ValuationForm
from main.models import *

#A temporary view
def render_form(request):    
    post = Post.objects.get_or_create(title = 'Test')[0]    
    form = ValuationForm(obj = post)
    form_html = render_to_string('valuate/form.html', {'form': form}, context_instance = RequestContext(request))    
    return HttpResponse(form_html)

@csrf_protect
@require_POST
def submit(request):    
    form = ValuationForm(request.POST)
    if form.is_valid():
        valuation = form.save(request)
        return HttpResponse('Valid Form')
    return HttpResponse('Invalid Form')        
    return HttpResponseRedirect(request.REQUEST.get('next', request.META.get('HTTP_REFERER', '/')))    
