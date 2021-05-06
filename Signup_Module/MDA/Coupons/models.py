from django.db import models
import random, datetime
from django.contrib.auth.models import User


class Coupon_SU(models.Model):

    CATEGORY = (
        ('Admin', 'Admin'),
        ('Member', 'Member')
    )

    Name = models.CharField(max_length=10, null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    Directory = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=10, unique=True, null=False)
    description = models.TextField(default=None, blank=True, null=True)
    valid_from = models.DateField(default=datetime.date.today)
    valid_till = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code