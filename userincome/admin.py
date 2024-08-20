from django.contrib import admin
from .models import UserIncome, Source
# Register your models here.



class UserIcomeAdmin(admin.ModelAdmin):
    list_display =('owner', 'amount', 'source', 'description', 'date',)
    search_fields =( 'amount', 'source', 'description', 'date',)
    list_per_page= 20
    
    
admin.site.register(UserIncome, UserIcomeAdmin)
admin.site.register(Source)