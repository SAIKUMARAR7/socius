from django import forms
from socius.models import memberdirectory
from socius.models import DirectoryMembers

class DirectoryCreationForm(forms.ModelForm):
    class Meta:
        model=memberdirectory
        fields=('DirectoryName','img','Description','MemberLimit','DirectoryId')

class DirectoryjoinForm(forms.ModelForm):
    class Meta:
        model=DirectoryMembers
        fields=('Name','Bio','DirectoryId')
