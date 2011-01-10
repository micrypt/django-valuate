from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType as CT
from valuate.models import Rating, Like, RATING_CHOICES

class AbstractValuateForm(forms.Form):
    '''
    An abstract form for being inherited by forms for various valuate models.
    '''
    content_type  = forms.IntegerField(widget=forms.HiddenInput)
    object_pk     = forms.CharField(widget=forms.HiddenInput)    
    submit_button_text = 'Submit'
    disabled = False
    def __init__(self, data=None, initial = {}, obj = None, request = None, *args, **kwargs):        
        if obj:
            ctype = CT.objects.get_for_model(obj)
            initial['content_type'] = ctype.id 
            initial['object_pk'] = obj.pk            
            if request:
                Model = self.get_model()
                valuate_instances_for_obj = Model.objects.filter(content_type=ctype, object_pk = obj.pk)
                try:
                    if valuate_instances_for_obj.get(user = request.user) or valuate_instances_for_obj.get(user = request.COOKIES.get('sessionid', '')):
                        self.disabled = True
                    
                except Model.DoesNotExist:                                
                    pass
                
        return super(AbstractValuateForm, self).__init__(data=data, initial = initial, *args, **kwargs)

    def get_model_fields(self, request):
        '''
        Get the fields dictionary for the valuate models. Can be
        overriden by subclasses with models which have different fields.
        '''
        cleaned_data = self.cleaned_data
        cleaned_data['content_type'] = CT.objects.get(id = cleaned_data['content_type'])
        cleaned_data['session'] = request.COOKIES.get('sessionid', '')
        cleaned_data['ip_address'] = request.META.get('REMOTE_ADDR', '')        
        if request.user.is_authenticated:
            cleaned_data['user'] = request.user        
        return cleaned_data

    def get_model(self):
        '''
        To be overriden by Sub classes.
        '''
        pass

    def save(self, request, commit = True):
        Model = self.get_model()
        obj = Model(**self.get_model_fields(request))
        if commit:
            obj.save()
        return obj
       
class RatingForm(AbstractValuateForm):    
    rating = forms.ChoiceField(label = _('rating'), choices = RATING_CHOICES, initial=3)
    content_type  = forms.IntegerField(widget=forms.HiddenInput)
    object_pk     = forms.CharField(widget=forms.HiddenInput)

    target = 'valuate-rating'
    submit_button_text = 'Rate'

    def get_model(self):
        return Rating

class LikeForm(AbstractValuateForm):
    target = 'valuate-like'
    submit_button_text = 'Like'

    def get_model(self):
        return Like
