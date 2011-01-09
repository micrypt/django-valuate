from django import forms
from valuate.models import ValuateAbstarctModel, Rating, Like
  
class RatingForm(forms.ModelForm):
    content_type  = forms.CharField(widget=forms.HiddenInput)
    object_pk     = forms.CharField(widget=forms.HiddenInput)    
    class Meta:
        model = Rating
        fields = ('rating',)


class LikeForm(forms.ModelForm):
    content_type  = forms.CharField(widget=forms.HiddenInput)
    object_pk     = forms.CharField(widget=forms.HiddenInput)    
    class Meta:
        model = Like
        fields = ()
