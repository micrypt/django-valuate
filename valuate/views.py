from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType as CT
from valuate.forms import ValuationForm

@csrf_protect
@require_POST
def submit(request):
    '''
    The submissions of valuation forms will be handled here.
    Ajax supported untested.
    '''
    form = ValuationForm(request)    
    success = False        
    if form.is_valid():        
        valuation = form.save()
        success = True
        redirect = request.REQUEST.get('next',
                                       request.META.get('HTTP_REFERER',
                                                        valuation.get_absoulte_url()))        
    else:        
        form.clear()
        redirect = '/'
    if not request.is_ajax() or request.POST.get('ajax', False):
        return HttpResponseRedirect(redirect)
    else:
        return HttpResponse(simplejson.dumps(success), mimetype='application/javascript')
