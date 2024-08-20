from django.contrib import admin
from .models import Profile, About
from django.utils.html import format_html


class ProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;">'.format(object.profile_image.url))
    thumbnail.short_description = 'Profile Picture'
    list_display =['thumbnail','user', 'name', 'phone_number', 'gender', 'date',]
    list_display_links=('thumbnail','user', 'name', 'phone_number',)
    search_fields =('name','phone_number',)
    ordering=('-date',)
    list_per_page= 20
    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(About)

