from django.db import models
from django.contrib.contenttypes.models import ContentType as CT

class ValuateManager(models.Manager):        
    def create_for_object(self, obj, *args, **kwargs):
        ctype, object_pk = CT.objects.get_for_model(obj), obj.pk
        return self.create(content_type = ctype, object_pk = object_pk, *args, **kwargs)

    def get_for_object(self, obj):
        ctype, object_pk = CT.objects.get_for_model(obj), obj.pk
        return self.filter(content_type = ctype, object_pk = object_pk)

    def get_count_for_object(self, obj):        
        return self.get_for_object(obj).count()


class RatingManager(ValuateManager):
    def get_avarage_score_for_object(self, obj):
        pass
