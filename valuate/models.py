from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType as CT
from django.core import urlresolvers
from django.contrib.auth.models import User
from valuate.managers import ValuationManager
import settings

class ValuationSettings:
    def __init__(self, name, choices_list):
        self.name = name
        self.choices_list = choices_list
        self.choices = self.get_choices_from_list()
        
    def get_choices_from_list(self):
        choices = []
        for i, choice in enumerate(self.choices_list):
            choices.append((i+1, choice))
        return tuple(choices)

VS = ValuationSettings
default_valuation_settings = ValuationSettings(
                                        getattr(settings, "VALUATION_OBJECT_NAME", 'Value'),
                                        getattr(settings, "VALUATION_OBJECT_CHOICES", ['Low', 'Medium', 'High'])
                                        )

valuate_template_var = getattr(settings, "VALUATION_TEMPLATE", False)

if valuate_template_var:
    if valuate_template_var=='rating':
        default_valuation_settings = VS('Rating', ['Bad', 'Poor', 'Average', 'Good', 'Excelent'])
    elif valuate_template_var=='like':
        default_valuation_settings = VS('Like', ['DisLike', 'Like'])
        
valuation_settings = default_valuation_settings

class Valuation(models.Model):    
    content_type = models.ForeignKey(CT,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk   = models.CharField(_('object ID'), max_length=200)
    content_object = generic.GenericForeignKey("content_type",
                                               "object_pk")
    user        = models.ForeignKey(User, verbose_name=_('user'),
                                   blank=True,
                                   null=True,
                                   related_name="%(class)s")
    session     = models.CharField(max_length = 200)
    value       = models.IntegerField(choices = valuation_settings.choices, default = len(valuation_settings.choices))
    ip_address  = models.IPAddressField(_('IP address'),
                                       blank=True,
                                       null=True)
    site        = models.ForeignKey(Site, verbose_name=_('site'),
                                   default = settings.SITE_ID)
    submit_date = models.DateTimeField(_('date/time submitted'),
                                       auto_now_add=True)    
    objects = ValuationManager()        
        
    def __unicode__(self):
        return '%s: "%s", %s: "%s"' %(unicode(self.content_type).title(), self.content_object, valuation_settings.name, self.get_value_display())
    
    def get_absolute_url(self):
        return self.content_object.get_absoulte_url()

    def save(self, request=None, *args, **kwargs):        
        if request:
            self.session = request.COOKIES.get('sessionid', '')
            self.ip_address = request.META.get('REMOTE_ADDR', '')
            if request.user.is_authenticated():
                self.user = request.user     
        return super(Valuation, self).save(*args, **kwargs)
