from django.db import models
from django.contrib.contenttypes.models import ContentType as CT
from django.db.models import Avg
import settings
Q = models.Q
default_vtype_pk = getattr(settings,'DEFAULT_VALUATION_TYPE_PK', 1)

class ValuationTypeManager(models.Manager):
    '''
    Manager for valuation type.
    '''
    def get_default_type(self, *args, **kwargs):
        '''
        Returns default type of valuation according to settings or else
        the one with pk
        '''
        default_vtype = self.get(pk=default_vtype_pk, *args, **kwargs)
        return default_vtype    

    def get_type(self, for_vtype=None, *args, **kwargs):
        '''
        Returns type according to the title if provided or else the default
        type.
        '''
        if for_vtype:            
            vtype=self.get(slug=for_vtype, *args, **kwargs)
        else:
            vtype=self.get_default_type(*args, **kwargs)
            
        return vtype
    

class ValuationManager(models.Manager):
    '''
    Manager for the valuation model. 
    '''    
    def create_for_object(self, obj, *args, **kwargs):
        '''
        Create a valuation instance for object
        '''
        content_type, object_pk = CT.objects.get_for_model(obj), obj.pk
        return self.create(content_type=content_type, object_pk=object_pk,
                           *args, **kwargs)

    def filter_for_obj(self, obj, *args, **kwargs):
        '''
        Filter the valuations according to the object.
        '''
        ctype, object_pk = CT.objects.get_for_model(obj), obj.pk        
        return self.filter(content_type=ctype, object_pk=object_pk, *args,
                            **kwargs)

    def get_by_obj_client(self, request, obj=None, content_type=None,
                          object_pk=None, *args, **kwargs):                    
        '''
        The instance of valuation which matches the provided object
        and client (user/session) info if exists. 
        '''
        is_authenticated = request.user.is_authenticated()        
        q_session = Q(session=request.COOKIES.get('sessionid', ''))
        q_user = Q(user=request.user) if is_authenticated else Q()
        if obj:
            valuations_for_obj = self.filter_for_obj(obj, *args, **kwargs)
        else:
            #Mostly used in post requests
            valuations_for_obj = self.filter(
                                 content_type=content_type,
                                 object_pk=object_pk,
                                 *args, **kwargs
                                 )
        valuations_for_obj_by_client = valuations_for_obj.filter(
                                        q_session|q_user
                                        )        
        if valuations_for_obj_by_client:
            return valuations_for_obj_by_client[0]
        else:
            return None

    def get_average_score(self, obj, *args, **kwargs):
        '''
        The average valuations score for an object
        '''
        return self.filter_for_obj(obj, *args, **kwargs).aggregate(Avg('choice__value'))['choice__value__avg']
        
    def get_count(self, obj, *args, **kwargs):
        '''
        The number of valuations for the object.
        '''        
        return self.filter_for_obj(obj, *args, **kwargs).count()

    def get_full_status(self, obj, *args, **kwargs):
        '''
        Get the details about the score count corresponding to each choice
        for the object. Currently template based.
        '''
        valuations = self.filter_for_obj(obj, *args, **kwargs)
        return valuations
    
    def get_count_for_choice(self, obj, choice, *args, **kwargs):
        '''
        Get the score count for an object for a perticular choice.
        '''        
        return self.get_count(obj, choice__name=choice, *args, **kwargs)
