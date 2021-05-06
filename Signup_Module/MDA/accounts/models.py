from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    coupon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


