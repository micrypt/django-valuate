from django.contrib import admin
from valuate.models import Rating, Like

class BaseValuateAdmin(admin.ModelAdmin):    
    list_display = ('content_object', 'content_type', 'submit_date', 'value')
    list_filter = ['content_type', 'submit_date']    
    date_hierarchy = 'submit_date'    

admin.site.register(Rating, BaseValuateAdmin)
admin.site.register(Like, BaseValuateAdmin)
