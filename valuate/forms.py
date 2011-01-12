from django import forms
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType as CT
from valuate.models import Valuation as V

class ValuationForm(forms.ModelForm):
    content_type  = forms.ModelChoiceField(queryset=CT.objects.all(), widget=forms.HiddenInput)
    object_pk     = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, request, data=None, initial = {}, obj = None,
                 instance = None, *args, **kwargs):
        self.request = self.process_request(request)
        if obj:
            ctype = CT.objects.get_for_model(obj)
            initial['content_type'] = ctype
            initial['object_pk'] = obj.pk            
            instance = self.get_instance(request, obj)
            
        if request.POST:            
            instance = self.get_instance_for_post(request)
            data = request.POST

        return super(ValuationForm, self).__init__(data=data,
                                                   initial=initial,
                                                   instance=instance,
                                                   *args, **kwargs)            

    def clear(self):        
        try:
            self.instance.delete()
        except AssertionError:
            pass
            
    def get_instance(self, request, *args, **kwargs):
        return  V.objects.get_by_obj_client(request,
                                            *args, **kwargs)        

    def get_instance_for_post(self, request):
        return self.get_instance(request,
                                 content_type=request.POST['content_type'],
                                 object_pk=request.POST['object_pk'])

    def process_request(self,request):
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        if not request.COOKIES.get('sessionid', None):
            request.session.set_test_cookie()                        
        return request
    
    def save(self, *args, **kwargs):     
        valuation = super(ValuationForm, self).save(commit=False,
                                                    *args, **kwargs)
        valuation.save(self.request)
        return valuation
    
    class Meta:
        model = V
        fields = ('content_type', 'object_pk', 'value')
