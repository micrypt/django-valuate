from django.db import models
from django.contrib.contenttypes.models import ContentType as CT
from django.db.models import Avg
from valuate.management import valuation_settings as vs
Q = models.Q

class ValuationManager(models.Manager):
    '''
    Manager for the valuation model. 
    '''
    def create_for_object(self, obj, *args, **kwargs):
        '''
        Create a valuation instant for object
        '''
        content_type, object_pk = CT.objects.get_for_model(obj), obj.pk
        return self.create(content_type=content_type, object_pk=object_pk,
                           *args, **kwargs)

    def filter_for_obj(self, obj, *args, **kwargs):
        '''
        Filter the valuations according to the object.
        '''
        ctype, object_pk = CT.objects.get_for_model(obj), obj.pk
        return self.filter(content_type=ctype, object_pk=object_pk,
                           *args, **kwargs)

    def get_by_obj_client(self, request, obj=None, content_type=None,
                          object_pk = None):                    
        '''
        The instance of valuation which matches the provided object
        and client (user/session) info if exists. 
        '''
        is_authenticated = request.user.is_authenticated()        
        q_session = Q(session=request.COOKIES.get('sessionid', ''))
        q_user = Q(user=request.user) if is_authenticated else Q()
        if obj:
            valuations_for_obj = self.filter_for_obj(obj)
        else:
            valuations_for_obj = self.filter(
                                 content_type=content_type,
                                 object_pk=object_pk
                                 )
        valuations_for_obj_by_client = valuations_for_obj.filter(
                                        q_session|q_user
                                        )

        if valuations_for_obj_by_client:
            return valuations_for_obj_by_client[0]
        else:
            return None

    def get_average_score(self, obj):
        '''
        The average valuations score for an object
        '''
        return self.filter_for_obj(obj).aggregate(Avg('value'))['value__avg']
        
    def get_count_for_object(self, obj):
        '''
        The number of valuations for the object.
        '''
        return self.get_for_object(obj).count()

    def get_full_status(self, obj):
        '''
        Get the details about the score count corresponding to each choice
        for the object.
        '''
        valuations_for_obj = self.filter_for_obj(obj)
        status = {}
        for choice in vs.choices_list:            
            status[choice] = valuations_for_obj.filter(value=vs.get_choice_value(choice)).count()
        return status        
    
    def get_choice_count(self, obj, choice):
        '''
        Get the score count for an object for a perticular choice.
        '''
        return self.filter_for_obj(obj, value=vs.get_choice_value(choice)).count()
