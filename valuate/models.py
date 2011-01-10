from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.contrib.auth.models import User
from valuate.managers import ValuateManager
import settings

FORCE_UNIQUE_BY_DB = True

RATING_CHOICES = (
        (1, 'Bad'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excelent'),
    )

class ValuateAbstarctModel(models.Model):
    content_type = models.ForeignKey(ContentType,
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
    ip_address  = models.IPAddressField(_('IP address'),
                                       blank=True,
                                       null=True)
    site        = models.ForeignKey(Site, verbose_name=_('site'),
                                   default = settings.SITE_ID)
    submit_date = models.DateTimeField(_('date/time submitted'),
                                       auto_now_add=True)    

    objects = ValuateManager()    
    
    def __unicode__(self):
        return '%s (a %s), %s' %(self.content_object, self.content_type, self.__class__.__name__)

    def get_absolute_url(self):
        return self.content_object.get_absoulte_url()
    
    class Meta:
        abstract=True
        if FORCE_UNIQUE_BY_DB:
            unique_together = (('session', 'content_type', 'object_pk'), ('user', 'content_type', 'object_pk'))


class Rating(ValuateAbstarctModel):    
    rating = models.IntegerField(choices=RATING_CHOICES)    
    def __unicode__(self):        
        return '%s: %s' %(super(Rating, self).__unicode__(), self.get_rating_display())    

    def value(self):
        return self.get_rating_display()
        
class Like(ValuateAbstarctModel):    
    def value(self):
        return 'Like'
    value.allow_tags = True
        
