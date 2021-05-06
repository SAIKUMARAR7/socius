from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from events.forms import EventCreationForm
from .models import  Event



def createEvent(request):
    
    
    if request.method == 'POST':
        event_form = EventCreationForm(request.POST)
        if event_form.is_valid():

            user = request.user
            event_title = request.POST['event_title']
            event_description = request.POST['event_description']
            event_date = request.POST['event_date']
            event_location = request.POST['event_location']
            obj1 = Event(
                event_title=event_title,
                event_description=event_description,
                event_date=event_date,
                event_location=event_location,
                user=user
            )
            obj1.save()
            messages.success(request, 'Event is created Successfully!')

            return redirect('createEvent')

    else:
        event_form = EventCreationForm()
    
    context = {'event_form': event_form}
    return render(request, 'events/eventForm.html', context)
    
    
    
def events_table(request):
    context = {}
    user = request.user
    events = Event.objects.filter(user=user)
    context['events'] = events
    return render(request, 'events/event_table.html', context)
    
    
    
    # context = {}

    # current_user = Event.objects.filter(user = request.user.id)
    # event_form = EventCreationForm(request.POST)
    # if request.method == "POST":
    #     if event_form.is_valid():
    #         event_form.save()
    #         messages.success(request, 'Event is created Successfully!')
    #         return redirect('createEvent')

    # else:
    #     event_form = EventCreationForm()
    
    # context['event_form'] = event_form
    # context['current_user'] = current_user

    # return render(request, 'userprofile/eventForm.html', context)






    # user = request.user
    # eventForm = EventCreationForm(request.POST)
    # if eventForm.is_valid():
    #     obj = eventForm.save()
    #     current_user = Event.objects.filter(user=user.id).first()
    #     obj.user = current_user
    #     obj.save()
    #     eventForm = EventCreationForm()
    
    # context['eventForm'] = eventForm
    # return render(request, "userprofile/eventForm.html", context)
    
    # if request.user:
    #     if request.method == 'POST':
    #         if eventForm.is_valid():
    #             eventForm.save()
    #             messages.success(request, 'Coupon Code is generated successfully!')
    #             return redirect('createEvent') 
    
    # else:
    #     eventForm = EventCreationForm()

    # context['eventForm'] = eventForm


    # return render(request, 'userprofile/eventForm.html', context)
