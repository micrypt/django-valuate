from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType as CT
from django.core import urlresolvers
from django.contrib.auth.models import User
from valuate.managers import ValuationManager, ValuationTypeManager

import settings

class ValuationType(models.Model):
    title = models.CharField(_('title'), max_length=50)

    objects = ValuationTypeManager()

    def __unicode__(self):
        return self.title.title()

class ValuationChoice(models.Model):
    name = models.CharField(_('choice'), max_length=50)
    value = models.IntegerField(_('value'))
    vtype = models.ForeignKey(ValuationType,
                              verbose_name=_('valuation type'))

    def __unicode__(self):
        return self.name.title()

class Valuation(models.Model):
    '''
    The valuation model.
    '''           
    content_type = models.ForeignKey(CT, verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk   = models.CharField(_('object ID'), max_length=200)
    content_object = generic.GenericForeignKey("content_type",
                                               "object_pk")
    user        = models.ForeignKey(User, verbose_name=_('user'),
                                   blank=True,
                                   null=True,
                                   related_name="%(class)s")
    session     = models.CharField(_('session'), max_length = 200)
    vtype       = models.ForeignKey(ValuationType,
                                    verbose_name=_('type'))
    choice      = models.ForeignKey(ValuationChoice,
                                    verbose_name=_('choice'))
    ip_address  = models.IPAddressField(_('IP address'),
                                       blank=True,
                                       null=True)
    site        = models.ForeignKey(Site, verbose_name=_('site'),
                                   default = settings.SITE_ID)
    submit_date = models.DateTimeField(_('date/time submitted'),
                                       auto_now_add=True)    
    objects = ValuationManager()        
    def __unicode__(self):
        return '%s: "%s", %s: "%s"' %(unicode(self.content_type).title(),
                                      self.content_object,
                                      self.choice.vtype,
                                      self.choice)

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
        self.vtype = self.choice.vtype
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
        pass
        #Prevenet multiple submissions for same client-object pair. 
        unique_together = (('vtype', 'user', 'content_type', 'object_pk'),
                           ('vtype', 'session', 'content_type', 'object_pk'))
