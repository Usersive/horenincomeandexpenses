from django.contrib import admin
from .models import Expenses, Category
# Register your models here.



class ExpensesAdmin(admin.ModelAdmin):
    list_display =('owner', 'amount', 'category', 'description', 'date',)
    search_fields =('amount','category', 'description', 'date',)
    list_per_page= 20



class CategoryAdmin(admin.ModelAdmin):
    list_display =('name',)
    
    
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(Category, CategoryAdmin)