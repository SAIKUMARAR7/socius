from django.forms import ModelForm
from django import forms
from .models import Event, EventRegistration


class DateInput(forms.DateInput):
    input_type = "date"
    input_formats = "dd/mm/yyyy"


class EventCreationForm(ModelForm):
    event_date = forms.DateField(widget=DateInput)
    class Meta:
        model = Event
        fields = ("event_title", "event_description", "event_date", "event_location")


class RegisterForEvent(ModelForm):
    class Meta: 
        model = EventRegistration
        fields = '__all__'