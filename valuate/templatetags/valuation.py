from django import template
from valuate.forms import ValuationForm
register = template.Library()

@register.inclusion_tag('valuate/form.html', takes_context=True)
def render_valuation_form(context, obj):
    request = context['request']
    form = ValuationForm(request, obj = obj)
    return {'form':form}
