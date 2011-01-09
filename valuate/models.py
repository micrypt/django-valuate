from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.contrib.auth.models import User
import settings

def get_object_ctype_pk(obj):
    ctype = ContentType.objects.get_for_model(obj)
    object_pk = obj.pk
    return ctype, object_pk

class ValuateManager(models.Manager):        
    def create_for_object(self, obj, *args, **kwargs):
        ctype, object_pk = get_object_ctype_pk(obj)
        return self.create(content_type = ctype, object_pk = object_pk, *args, **kwargs)

    def get_for_object(self, obj):
        ctype, object_pk = get_object_ctype_pk(obj)
        return self.filter(content_type = ctype, object_pk = object_pk)

    def get_count_for_object(self, obj):        
        return self.get_for_object(obj).count()
    
class ValuateAbstarctModel(models.Model):
    content_type   = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_pk      = models.CharField(_('object ID'), max_length=200)
    content_object = generic.GenericForeignKey("content_type", "object_pk")
    user        = models.ForeignKey(User, verbose_name=_('user'),
                    blank=True, null=True, related_name="%(class)s")
    session     = models.CharField(max_length = 200, editable = False )
    site        = models.ForeignKey(Site, verbose_name=_('site'), default = settings.SITE_ID)
    submit_date = models.DateTimeField(_('date/time submitted'), auto_now_add=True)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)

    objects = ValuateManager()
    def __unicode__(self):
        return '%s(%s), %s' %(self.content_object, self.content_type, self.__class__.__name__)
    
    class Meta:
        abstract=True        


class Rating(ValuateAbstarctModel):
    CHOICES = (
        (1, 'Bad'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excelent'),
    )
    rating = models.IntegerField(choices=CHOICES)
    def __unicode__(self):        
        return '%s: %s' %(super(Rating, self).__unicode__(), self.get_rating_display())    

class Like(ValuateAbstarctModel):    
    pass

        
