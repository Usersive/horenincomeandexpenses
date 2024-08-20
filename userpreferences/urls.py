

from django.urls import path
from .import views


urlpatterns = [
    path('preferences/', views.index, name='preferences'),
    path('add_event/', views.add_event, name='add_event'),
    path('event_delete/<int:id>', views.event_delete, name='event_delete'),
    
]
