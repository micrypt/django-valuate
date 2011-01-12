from django.db import models
from django.contrib.contenttypes.models import ContentType as CT
Q = models.Q

class ValuationManager(models.Manager):        
    def create_for_object(self, obj, *args, **kwargs):
        content_type, object_pk = CT.objects.get_for_model(obj), obj.pk
        return self.create(content_type = content_type, object_pk = object_pk, *args, **kwargs)

    def filter_for_obj(self, obj):
        ctype, object_pk = CT.objects.get_for_model(obj), obj.pk
        return self.filter(content_type = ctype, object_pk = object_pk)

    def get_count_for_object(self, obj):        
        return self.get_for_object(obj).count()

    def get_by_obj_client(self, request, obj=None, content_type=None,
                          object_pk = None):                    
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
