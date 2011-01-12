from django.contrib import admin
from valuate.models import Valuation

class ValuationAdmin(admin.ModelAdmin):    
    list_display = ('value', 'content_object', 'content_type', 'submit_date', 'user', 'session')
    list_filter = ['value', 'content_type', 'submit_date']
    search_fields = ['user__username', 'user__email', 'content_type__app_label', 'ip_address']
    date_hierarchy = 'submit_date'    

admin.site.register(Valuation, ValuationAdmin)
