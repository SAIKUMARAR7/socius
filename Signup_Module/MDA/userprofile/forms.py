from django import forms
from .models import Profile,profilePic,Skills,Speciality,Certificate,Testimonial,Education
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type = "date"
    input_formats = "dd/mm/yyyy"

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['firstName','lastName','email','altEmail','phone','altPhone','address','city','state','country','postalCode','aboutMe']

class ProfilePicForm(ModelForm):
    class Meta:
        model = profilePic
        fields = ['image','status','tagLine']
       
class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = ['skill']

class SpecialityForm(ModelForm):
    class Meta:
        model = Speciality
        fields = ['speciality']

class CertificateForm(ModelForm):
    issuedDate = forms.DateField(widget=DateInput)
    expiryDate = forms.DateField(widget=DateInput)
    class Meta:
        model = Certificate
        fields = ['name' ,'issuingOrg','issuedDate' ,'expiryDate','credentialId' ,'credentialUrl' ,'description']

class TestimonialForm(ModelForm):
    issuedDate = forms.DateField(widget=DateInput)
    class Meta:
        model = Testimonial
        fields =[ 'attestant' ,'issuedDate' ,'services' , 'designation', 'location' ,'description']

class EducationForm(ModelForm):
    startDate = forms.DateField(widget=DateInput)
    endDate = forms.DateField(widget=DateInput)
    class Meta:
        model = Education
        fields = ['institute', 'degree', 'branch','grade','startDate', 'endDate' ,'description']
