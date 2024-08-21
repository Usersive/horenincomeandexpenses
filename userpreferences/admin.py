from django.contrib import admin
from .models import UserPreferences, Event
# Register your models here.



class EventAdmin(admin.ModelAdmin):
    list_display =('name',  'description', 'event_date',)
    list_display_links=('name',  'description',)
    search_fields =('name',  'description',)
    
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display =['user', 'currency',]
    list_display_links =['user', 'currency',]

admin.site.register(UserPreferences, UserPreferencesAdmin)
admin.site.register(Event, EventAdmin)



