from django.db import models
from django.contrib.auth.models import User
from socius.models import UserList


'''from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.TextField(default='')
    tagline = models.TextField(default='')
    status = models.TextField(default='')
    def __str__(self):
        return self.user.username'''


class Event(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event_title = models.CharField(max_length=100, null=True)
    event_description = models.TextField(default=None, null=True)
    event_date = models.DateField()
    event_location = models.CharField(max_length=100, null=True)


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=100, null=True)
    # member