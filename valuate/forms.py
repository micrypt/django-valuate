from django import forms
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType as CT
from valuate.models import Valuation as V, ValuationType as VT, ValuationChoice as VC

class ValuationForm(forms.ModelForm):
    '''
    The form for valuation model. Exclusively requires the `request`
    context for checking previous object instances according to the
    `current session` or `user` and also passing these variables to
    the model save method while saving the form.
    '''

    def __init__(self, request, data=None, initial={}, obj=None,
                 instance=None, vtype=None, *args, **kwargs):
        '''
        Fills `content_type` and `object_pk` according to object and
        processes `request` data
        '''                    
        self.request = self.process_request(request)
        if obj:            
            ctype = CT.objects.get_for_model(obj)
            initial['content_type'] = ctype
            initial['object_pk'] = obj.pk
            initial['vtype'] = vtype
            instance = self.get_instance(request, obj=obj,
                                         vtype=vtype)            
            
        if request.POST:            
            instance = self.get_instance_by_post_data(request)            
            data = request.POST
        super(ValuationForm, self).__init__(data=data,
                                            initial=initial,
                                            instance=instance,
                                            *args, **kwargs)
    
    content_type= forms.ModelChoiceField(queryset=CT.objects.all(),
                                         widget=forms.HiddenInput)
    object_pk   = forms.CharField(widget=forms.HiddenInput)
    vtype       = forms.ModelChoiceField(queryset=VT.objects.all(),
                                         widget=forms.HiddenInput)

    def clear(self):
        '''
        Clear the instance if an invalid form with instance is submitted. 
        '''
        self.instance.delete()
        try:
            self.instance.delete()
        except AssertionError:
            pass

    def get_id(self):
        '''
        Returns the id for the html form.
        '''
        ctype = self.data.get('content_type', self.initial.get('content_type','').id)
        object_pk = self.data.get('object_pk', self.initial.get('object_pk',''))
        return "valuate_%s_%s" %(ctype, object_pk)
    
    def get_instance(self, request, *args, **kwargs):
        '''
        Returns instance according to the object and request (user,
        session). Needs either object or content_type, object_pk as
        arguments as does `get_by_obj_client`
        '''
        instance = V.objects.get_by_obj_client(request,
                                               *args, **kwargs)        
        return  instance

    def get_instance_by_post_data(self, request, *args, **kwargs):
        '''
        Returns instance according to the post data from request        
        '''
        vtype=request.POST['vtype']
        instance = self.get_instance(request,
                             content_type=request.POST['content_type'],
                             object_pk=request.POST['object_pk'],
                             vtype=request.POST['vtype'],
                             *args, **kwargs)
        return instance

    def process_request(self,request):
        '''
        Prcesses the request to ensure if the session cookie is set.
        TODO: Need to find a better alternative.
        '''
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        if not request.COOKIES.get('sessionid', None):
            request.session.set_test_cookie()                        
        return request
    
    def save(self, *args, **kwargs):
        '''
        Saves the model with the request variable. 
        '''        
        valuation = super(ValuationForm, self).save(commit=False,
                                                    *args, **kwargs)
        valuation.save(self.request)        
        return valuation
    
    class Meta:
        model = V
        fields = ('content_type', 'object_pk', 'choice')
