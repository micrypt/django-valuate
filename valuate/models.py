from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType as CT
from django.core import urlresolvers
from django.contrib.auth.models import User
from valuate.managers import ValuationManager
from valuate.management import valuation_settings as vs
import settings

class Valuation(models.Model):
    '''
    The valuation model.
    '''    
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
    session     = models.CharField(_('session'), max_length = 200)
    value       = models.IntegerField(_(vs.name), choices = vs.choices)
    ip_address  = models.IPAddressField(_('IP address'),
                                       blank=True,
                                       null=True)
    site        = models.ForeignKey(Site, verbose_name=_('site'),
                                   default = vs.site)
    submit_date = models.DateTimeField(_('date/time submitted'),
                                       auto_now_add=True)    
    objects = ValuationManager()        
    def __unicode__(self):
        return '%s: "%s", %s: "%s"' %(unicode(self.content_type).title(),
                                      self.content_object,
                                      vs.name.title(),
                                      self.get_value_display())
    
    def get_absoulte_url(self):
        try:
            content_object_url = self.content_object.get_absoulte_url()
        except:
            content_object_url = None
            
        if content_object_url:            
            return content_object_url
        else:
            return '/'
            

    def save(self, request=None, *args, **kwargs):
        '''
        Save method overriden if `request` var is supplied.    
        '''
        if request:                                                
            sessionid = request.session.session_key
            if sessionid:
                self.ip_address = request.META.get('REMOTE_ADDR', '')
                self.session = sessionid
                if request.user.is_authenticated():
                    self.user = request.user            
                return super(Valuation, self).save(*args, **kwargs)
        else:
            return super(Valuation, self).save(*args, **kwargs)

    class Meta:
        #Prevenet multiple submissions for same client-object pair. 
        unique_together = (('user', 'content_type', 'object_pk'), ('session', 'content_type', 'object_pk'))
