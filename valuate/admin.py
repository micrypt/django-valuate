from django.contrib import admin
from valuate.models import Valuation, ValuationType, ValuationChoice

class ValuationChoiceInline(admin.TabularInline):
    model = ValuationChoice
    extra = 3
	
class ValuationTypeAdmin(admin.ModelAdmin):
    list_display=('title',)
    inlines = [ValuationChoiceInline]
    prepopulated_fields = {"slug": ("title",)}

class ValuationAdmin(admin.ModelAdmin):    
    list_display = ('choice', 'vtype', 'content_object', 'content_type', 'submit_date', 'user', 'session')
    list_filter = ['vtype', 'choice', 'content_type', 'submit_date']
    search_fields = ['user__username', 'user__email', 'content_type__app_label', 'ip_address']
    date_hierarchy = 'submit_date'    

admin.site.register(ValuationType, ValuationTypeAdmin)
admin.site.register(Valuation, ValuationAdmin)

