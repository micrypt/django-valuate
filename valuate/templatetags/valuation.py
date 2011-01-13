from django import template
from valuate.models import Valuation
from valuate.forms import ValuationForm
register = template.Library()
VOs=Valuation.objects

'''
Defines the templatetags for easy plugging of valuations with objects.

TODO:
 - Write ajax submission field tags.
 - Better template Nodes based and more interactive templatetags like
   django comments framework tags. 
'''

def get_ajax_fields(context, obj):
    '''
    TODO: Complete this function
    '''
    fields = {}    
    return fields

def get_valuation_score(context, obj):
    '''
    Returns the average score of the object according to the valuations.
    '''
    return VOs.get_average_score(obj)
    
def get_choice_count(context, obj, choice):
    '''
    Returns the score count for a perticular choice of an object. Choice
    should be provided with quotes (as string)
    '''
    return VOs.get_choice_count(obj, choice)

def render_valuation_status(context, obj):
    '''
    Renders the status according to the score of various choices.
    Override template: 'valuate/status.html' for modifying the look.
    '''
    return {'status':VOs.get_full_status(obj)}

def render_valuation_form(context, obj, request=None):
    '''
    Renders the valuation form for the object.
    Override template: 'valuate/form.html' for modifying the look.
    '''
    if not request:
        request = context['request']
    form = ValuationForm(request, obj = obj)
    return {'form':form}

register.simple_tag(takes_context=True)(get_choice_count)
register.simple_tag(takes_context=True)(get_valuation_score)
register.inclusion_tag('valuate/form.html', takes_context=True)(render_valuation_form)
register.inclusion_tag('valuate/status.html', takes_context=True)(render_valuation_status)
