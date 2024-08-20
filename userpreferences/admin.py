from django.contrib import admin
from .models import UserPreferences, Event
# Register your models here.



class EventAdmin(admin.ModelAdmin):
    list_display =('name',  'description', 'event_date',)
    list_display_links=('name',  'description',)
    search_fields =('name',  'description',)

admin.site.register(UserPreferences)
admin.site.register(Event, EventAdmin)



