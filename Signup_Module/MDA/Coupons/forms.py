from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from .models import Coupon_SU

class DateInput(forms.DateInput):
    input_type = "date"
    input_formats = "dd/mm/yyyy"


class Coupon_code_SU_(ModelForm):
    
    valid_from = forms.DateField(widget=DateInput)
    valid_till = forms.DateField(widget=DateInput)
    class Meta:
        model = Coupon_SU
        fields = "__all__"