from django import forms
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType as CT
from valuate.models import Valuation

class ValuationForm(forms.ModelForm):
    content_type  = forms.ModelChoiceField(queryset=CT.objects.all(), widget=forms.HiddenInput)
    object_pk     = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, data=None, initial = {}, obj = None, request=None, *args, **kwargs):        

        if obj:
            ctype = CT.objects.get_for_model(obj)
            initial['content_type'] = ctype
            initial['object_pk'] = obj.pk
            
        return super(ValuationForm, self).__init__(data=data, initial = initial, *args, **kwargs)            

    def save(self, request, *args, **kwargs):     
        valuations_for_obj = Valuation.objects.filter(
                                                      content_type=self.cleaned_data['content_type'],
                                                      object_pk=self.cleaned_data['object_pk']
                                                     )                
        is_authenticated = request.user.is_authenticated()
        q_session = Q(session=request.COOKIES.get('sessionid', ''))
        q_user = Q(user=request.user) if is_authenticated else Q()        
        valuations_for_obj_by_client = Valuation.objects.filter(q_session|q_user)                
        
        if valuations_for_obj_by_client:                    
            valuation = valuations_for_obj_by_client[0]
        else:
            valuation = super(ValuationForm, self).save(commit=False, *args, **kwargs)            
            valuation.session = request.COOKIES.get('sessionid', '')
            if is_authenticated:            
                valuation.user = request.user
                
        valuation.ip_address = request.META.get('REMOTE_ADDR', '')
        valuation.save()
        return valuation
    
    class Meta:
        model = Valuation
        fields = ('content_type', 'object_pk', 'value')
