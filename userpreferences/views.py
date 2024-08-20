from django.shortcuts import render, redirect, get_object_or_404
import os
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import UserPreferences, Event
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date  # Correctly import the date class
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
# Create your views here.



@login_required(login_url='/login')
def index(request):        
    currency_data =[]
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name': k, 'value': v})
     
    exists = UserPreferences.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences=UserPreferences.objects.get(user=request.user)
        
   
    if request.method =='GET':
        context ={
            'currencies': currency_data,
            'user_preferences': user_preferences,   
        }
        return render(request, 'userpreferences/index.html', context)
    
    else:
        currency =request.POST['currency']
        if exists:
            user_preferences.currency=currency
            user_preferences.save()
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changed save...')
        return render(request, 'userpreferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
    




# @login_required
# def add_event(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         description = request.POST['description']
#         event_date = request.POST['event_date']
#         Event.objects.create(user=request.user, name=name, description=description, event_date=event_date)
#         messages.success(request, "Event was created successfully...")
#         return redirect('add_event')
    
#     else:
#         today = date.today()  # Get today's date

#         # Separate today's events from other events
#         today_events = Event.objects.filter(user=request.user, event_date=today).order_by('-event_date')
#         other_events = Event.objects.filter(user=request.user).exclude(event_date=today).order_by('-event_date')

#         # Combine today's events with other events
#         events = list(today_events) + list(other_events)
        
#         paginator = Paginator(events, 1)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
        
#         context = {
#             'events': events,
#             'page_obj': page_obj,
#             'today': today,
#         }

#         return render(request, 'userpreferences/add_event.html', context)




@login_required
def add_event(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        event_date = request.POST['event_date']
        Event.objects.create(user=request.user, name=name, description=description, event_date=event_date)
        messages.success(request, "Event was created successfully...")
        return redirect('add_event')
    
    else:
        today = date.today()  # Get today's date

        # Separate today's events from other events
        today_events = Event.objects.filter(user=request.user, event_date=today).order_by('-event_date')
        other_events = Event.objects.filter(user=request.user).exclude(event_date=today).order_by('-event_date')

        # Combine today's events with other events
        events = list(today_events) + list(other_events)
        
        paginator = Paginator(events, 1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Prepare data for calendar
        event_data = {}
        for event in events:
            date_str = event.event_date.strftime('%Y-%m-%d')
            if date_str in event_data:
                event_data[date_str].append(event.description)
            else:
                event_data[date_str] = [event.description]

        context = {
            'events': events,
            'page_obj': page_obj,
            'today': today,
            'event_data': event_data,  # Add this line to pass event data to the template
        }

        return render(request, 'userpreferences/add_event.html', context)



@login_required(login_url='/login')
def event_delete(request, id):
    events = Event.objects.get(pk=id)
    events.delete()
    messages.success(request, "Event was removed")
    return redirect('add_event')  


#     return render(request, 'userpreferences/add_event.html', context)
    

# @login_required(login_url='/login')
# def event_delete(request, id):
#     event = Event.objects.get(pk=id)
#     event.delete()
#     messages.success(request, "Event was removed")
#     return redirect('add_event')  