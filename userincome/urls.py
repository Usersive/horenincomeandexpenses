from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .import views


urlpatterns = [
    path('income/', views.income, name='income'),
    path('add_income/', views.add_income, name='add_income'),
    path('income_edit/<int:id>', views.income_edit, name='income_edit'),
    path('income_delete/<int:id>', views.income_delete, name='income_delete'),
    path('search_income', csrf_exempt(views.search_income), name='search_income'),
    path('export_income_csv/', views.export_income_csv, name='export_income_csv'), 
    path('export_income_excel/', views.export_income_excel, name='export_income_excel'),
    path('export_income_pdf/', views.export_income_pdf, name='export_income_pdf'), 
    path('income_stats/', views.income_stats_view, name='income_stats'),  
    path('income_source_summary/', views.income_source_summary, name='income_source_summary'),
]
