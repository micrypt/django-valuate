from django import template
from django.contrib.contenttypes.models import ContentType as CT
from django.core.urlresolvers import reverse
from valuate.models import Valuation, ValuationType as VT
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

def get_valuation_ajax_fields(context, obj, as_var, for_vtype=None):
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
    vtype = VT.objects.get_type(for_vtype)
    choices = VT.objects.get_choice_queryset(for_vtype)
    choice = ''
    target = reverse('valuate-submit')        
    fields = {'chocies': choices, 'target':target,
              'vtype':vtype}
    initial_instance = VOs.get_by_obj_client(request, obj=obj,
                                             for_vtype=for_vtype)
    if initial_instance:
        fields['content_type'] = initial_instance.content_type.id
        fields['object_pk'] = initial_instance.object_pk
        fields['choice'] = initial_instance.choice
    else:    
        fields['content_type'] = CT.objects.get_for_model(obj).id
        fields['object_pk'] = obj.pk
        
    context[as_var]=fields
    return ''

def get_choice_count(context, obj, choice, for_vtype=None):
    '''
    Returns the score count for a perticular choice of an object. Choice
    should be provided with quotes (as string)
    '''
    return VOs.get_choice_count(obj, choice, for_vtype)

def get_valuation_form(context, obj, as_var, for_vtype=None, request=None):
    '''
    Adds the valuation form to the context with variable name as_var
    provided as a string.  
    User `form_name.target` to access the target for the post request.
    '''
    if not request:
        request = context['request']
    form = ValuationForm(request, obj = obj, for_vtype=for_vtype)
    form.fields['choice'].queryset=VT.objects.get_choice_queryset(for_vtype)
    context[as_var]=form
    return ''

def get_valuation_score(context, obj, for_vtype=None):
    '''
    Returns the average score of the object according to the valuations.
    '''
    return VOs.get_average_score(obj, for_vtype)    

def render_valuation_form(context, obj, for_vtype=None, request=None):
    '''
    Renders the valuation form for the object.
    Override template: 'valuate/form.html' for modifying the look.
    '''
    if not request:
        request = context['request']    
    form = ValuationForm(request, obj = obj, for_vtype=for_vtype)    
    form.fields['choice'].queryset=VT.objects.get_choice_queryset(for_vtype)
    return {'form':form}

def render_valuation_status(context, obj, for_vtype=None):
    '''
    Renders the status according to the score of various choices.
    Override template: 'valuate/status.html' for modifying the look.
    '''
    return {'status':VOs.get_full_status(obj, for_vtype)}

register.simple_tag(takes_context=True)(get_valuation_ajax_fields)
register.simple_tag(takes_context=True)(get_choice_count)
register.simple_tag(takes_context=True)(get_valuation_form)
register.simple_tag(takes_context=True)(get_valuation_score)
register.inclusion_tag('valuate/form.html', takes_context=True)(render_valuation_form)
register.inclusion_tag('valuate/status.html', takes_context=True)(render_valuation_status)
