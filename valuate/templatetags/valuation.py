from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType as CT
from django.core.urlresolvers import reverse
from valuate.models import Valuation, ValuationType as VT
from valuate.forms import ValuationForm

register = template.Library()
VOs=Valuation.objects

'''
Defines the templatetags for easy integration in templates directly.
'''

class BaseValuateNode(template.Node):
    methods = {}
    '''
    This is the base node for valuate app. Inherited by get and render
    template tags. The tags can use the default valuation type (pk=1 or
    DEFAULT_VALUATION_TYPE_PK setting. The valuation type if required can
    be specified by `for valuation_type` as arguments in the tag. 
    '''
    def __init__(self, parser, token, shift=0):
        '''
        Parses tag arguments and provides attributes for future methods.
        '''
        tokens = token.contents.split()
        self.vtype = VT.objects.get_type()
        self.as_varname = False
        method = self.get_method(tokens[1])
        if not method:
            raise template.TemplateSyntaxError("%r is not a valid method in %r tag" %(tokens[1], tokens[0]))
        else:
            self.method = method
            if tokens[1]=='choice_count':                
                if len(tokens) < 5 or not tokens[4]=='for_choice':
                    print 'called'
                    raise template.TemplateSyntaxError("Fourth argument in %r tag must be 'for_choice'" % tokens[0])
                else:
                    self.choice=tokens[5]
                shift+=2
        
        if not tokens[2]=='of':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'of'" % tokens[0])

        self.obj = parser.compile_filter(tokens[3])
        
        if len(tokens)==4+shift:
            pass
        
        elif len(tokens)==6+shift:
            if tokens[4+shift]=='for':
                self.vtype = VT.objects.get_type(tokens[5+shift])
                
            elif tokens[4+shift]=='as':
                self.as_varname = tokens[5+shift]

            else:
                raise template.TemplateSyntaxError("Argument #%d in %r tag must be 'for' (valuation type) or 'as' (variable name)" % (4+shift, tokens[0+shift]))

        elif len(tokens)==8+shift:
            if not tokens[4]=='for' and tokens[7]=='as':
                raise template.TemplateSyntaxError("Argument #%d in %r tag must be 'for' (valuation type) or and #%d 'as' (variable name)" %(4+shift, tokens[0], 6+shift))
            else:
                self.for_vtype = tokens[5]
                self.vtype = VT.objects.get_type(tokens[5])
                self.as_varname = tokens[7]

        else:
            raise template.TemplateSyntaxError("Number of arguments in %r tag can be %d, %d or %d and not %d" %(tokens[0], 3+shift, 5+shift, 7+shift, len(tokens)-1))

    def get_method(self, method):        
        return self.methods.get(method, None)    

class ValuateGetNode(BaseValuateNode):
    '''
    This node provides various statistics or properties about valuation of
    an object. The properties can be directly rendered or added to context
    by passing `as varname` in template tag.
    '''
    methods = {}
    
    def score(self, context):
        '''
        Returns the average score of the object according to the
        valuations.
        '''
        avg_score = VOs.get_average_score(self.obj.resolve(context),
                                          vtype=self.vtype)
        return round(avg_score, 2)    
    methods['score'] = score

    def form(self, context):
        '''
        Gets the valuation form in the context or directly. 
        User `form_name.target` to access the target for the post request.
        '''
        request = context['request']    
        form = ValuationForm(request, obj=self.obj.resolve(context),
                             vtype=self.vtype) 
        form.fields['choice'].queryset=self.vtype.choice_queryset()
        form.fields['choice'].label=self.vtype.title
        return form
    methods['form'] = form

    def ajax_fields(self, context):
        '''
        Get the fields as dictionary required for an ajax post request in the
        context or directly.
        
        Variables available:
        For post request: 'content_type','object_pk', 'choice' (to be selected
        by user, can have an initial value if user has already submitted once)
        'choices': dictionary of choices for user to provide the 'value' data.
        'target': target for the request.
        'vtype'": the valuation type. 
        On a successfull request, true will be retuned. 
        If you are not using a popular javascript liberary, pass on a POST
        variable with name `ajax` and a `true` value.
        '''
        request = context['request']
        vtype = self.vtype
        obj = self.obj.resolve(context)
        choices = vtype.choice_queryset()
        choice = ''
        target = reverse('valuate-submit')        
        fields = {'chocies': choices, 'target':target,
                  'vtype':vtype}
                
        initial_instance = VOs.get_by_obj_client(request, obj=obj,
                                                 vtype=vtype)        
        if initial_instance:            
            fields['content_type'] = initial_instance.content_type.id
            fields['object_pk'] = initial_instance.object_pk
            fields['choice'] = initial_instance.choice
        else:    
            fields['content_type'] = CT.objects.get_for_model(obj).id
            fields['object_pk'] = obj.pk
    
        return fields
    methods['ajax_fields'] = ajax_fields

    def choice_count(self, context):
        '''
        Returns the score count for a perticular choice of an object. Choice
        should be provided with quotes (as string)
        '''
        return VOs.get_count_for_choice(self.obj.resolve(context),
                                        choice=self.choice,
                                        vtype=self.vtype)
    methods['choice_count'] = choice_count
    
    def render(self, context):
        result = self.method(self, context)
        
        if self.as_varname:
            context[self.as_varname] = result
            return ''
        else:
            return result
    
class ValuateRenderNode(BaseValuateNode):
    '''
    This nodes render directly through an html template. Templates can be
    overridden at templates/valuate/*.html    
    '''
    methods = {}
    def form(self, context):
        '''
        Renders the valuation form for the object.
        Override template: 'valuate/form.html' for modifying the look.
        '''
        form = ValuationForm(context['request'],
                             obj=self.obj.resolve(context),
                             vtype=self.vtype)
        form.fields['choice'].queryset=self.vtype.choice_queryset()
        form.fields['choice'].label=self.vtype.title
        context['form']=form
        return render_to_string('valuate/form.html', context)
    methods['form']=form

    def status(self, context):
        context['status']=VOs.get_full_status(self.obj.resolve(context),
                                              vtype=self.vtype)        
        return render_to_string('valuate/status.html', context)
    methods['status']=status
    
    def render(self, context):
        '''
        Renders the status according to the score of various choices.
        Override template: 'valuate/status.html' for modifying the look.
        '''
        result = self.method(self, context)
        return result

def do_get_valuate(parser, token):
    return ValuateGetNode(parser, token)

def do_render_valuate(parser, token):
    return ValuateRenderNode(parser, token)

register.tag('get_valuate', do_get_valuate)
register.tag('render_valuate', do_render_valuate)
