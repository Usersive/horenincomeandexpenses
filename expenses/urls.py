from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .import views


urlpatterns = [
    path('expenses/', views.expenses, name='expenses'),
    path('add_expenses/', views.add_expenses, name='add_expenses'),
    path('expenses_edit/', views.expenses, name='expenses_edit'),
    path('expenses_edit/<int:id>', views.expenses_edit, name='expenses_edit'),
    path('expense_delete/<int:id>', views.expense_delete, name='expense_delete'),
    path('search_expenses', csrf_exempt(views.search_expenses), name='search_expenses'),
    path('expense_category_summary/', views.expense_category_summary, name='expense_category_summary'),
    path('expenses_stats/', views.expenses_stats_view, name='expenses_stats'),
    path('export_csv/', views.export_csv, name='export_csv'), 
    path('export_excel/', views.export_excel, name='export_excel'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
]
