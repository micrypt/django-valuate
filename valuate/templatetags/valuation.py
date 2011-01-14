from django import template
from django.contrib.contenttypes.models import ContentType as CT
from django.core.urlresolvers import reverse
from valuate.models import Valuation
from valuate.forms import ValuationForm
from valuate.management import valuation_settings as vs
register = template.Library()
VOs=Valuation.objects

'''
Defines the templatetags for easy plugging of valuations with objects.

TODO:
 - Better template Nodes based and more interactive templatetags like
   django comments framework tags. 
'''

def get_valuation_ajax_fields(context, obj, as_var):
    '''
    Adds the fields as dictionary required for an ajax post request to
    the context with variable name `as_var` provided as a string.
    Variables available:
    For post request: 'content_type','object_pk', 'value' (to be selected
    by user, can have an initial value if user has already submitted once)
    'choices': dictionary of choices for user to provide the 'value' data.
    'target': target for the request.
    On a successfull request, true will be retuned. 
    If you are not using a popular javascript liberary, pass on a POST
    variable with name `ajax` and a `true` value.
    '''
    request = context['request']
    initial_instance = VOs.get_by_obj_client(request, obj)
    if initial_instance:
        content_type = initial_instance.content_type.id
        object_pk = initial_instance.object_pk
        value = initial_instance.value        
    else:    
        content_type = CT.objects.get_for_model(obj).id
        object_pk = obj.pk
        value = None
    choices = vs.choices_dict_rev
    target = reverse('valuate-submit')
    fields = {'content_type': content_type, 'object_pk':object_pk, 'value':value, 'chocies': choices, 'target':target}    
    context[as_var]=fields
    return ''

def get_choice_count(context, obj, choice):
    '''
    Returns the score count for a perticular choice of an object. Choice
    should be provided with quotes (as string)
    '''
    return VOs.get_choice_count(obj, choice)

def get_valuation_form(context, obj, as_var, request=None):
    '''
    Adds the valuation form to the context with variable name as_var
    provided as a string.  
    User `form_name.target` to access the target for the post request.
    '''
    if not request:
        request = context['request']
    form = ValuationForm(request, obj = obj)
    context[as_var]=form 
    return ''

def get_valuation_score(context, obj):
    '''
    Returns the average score of the object according to the valuations.
    '''
    return VOs.get_average_score(obj)    

def render_valuation_form(context, obj, request=None):
    '''
    Renders the valuation form for the object.
    Override template: 'valuate/form.html' for modifying the look.
    '''
    if not request:
        request = context['request']
    form = ValuationForm(request, obj = obj)
    return {'form':form}

def render_valuation_status(context, obj):
    '''
    Renders the status according to the score of various choices.
    Override template: 'valuate/status.html' for modifying the look.
    '''
    return {'status':VOs.get_full_status(obj)}

register.simple_tag(takes_context=True)(get_valuation_ajax_fields)
register.simple_tag(takes_context=True)(get_choice_count)
register.simple_tag(takes_context=True)(get_valuation_form)
register.simple_tag(takes_context=True)(get_valuation_score)
register.inclusion_tag('valuate/form.html', takes_context=True)(render_valuation_form)
register.inclusion_tag('valuate/status.html', takes_context=True)(render_valuation_status)
