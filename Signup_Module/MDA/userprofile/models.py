from django.db import models
from django.contrib.auth.models import User
import datetime
from multi_email_field.fields import MultiEmailField
from PIL import Image
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20,default='')
    lastName = models.CharField(max_length=20,default='')

    email = models.EmailField(default='')
    altEmail = models.EmailField(default='',blank=True)
    phone = PhoneNumberField(blank=True)
    altPhone = PhoneNumberField(blank=True)

    address = models.CharField(max_length=150,blank=True,default='')
    city = models.CharField(max_length=30,blank=True,default='')
    state = models.CharField(max_length=30,blank=True,default='')
    country = models.CharField(max_length=20,blank=True,default='')
    postalCode = models.PositiveIntegerField(blank=True,default=0)

    aboutMe = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

##Foreign Key Tables##

class profilePic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='images')
    status = models.CharField(max_length=200 ,blank=True,default='')
    tagLine = models.CharField(max_length=100, blank=True,default='')


class Skills(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='userSkills',default='',null=True)
    skill = models.CharField(null=True,blank=True,max_length=100)

class Speciality(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='userSpeciality',default='',null=True)
    speciality = models.CharField(null=True,blank=True,max_length=100)


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='userCertificate',default='',null=True)
    name = models.CharField(max_length=100,default='')
    issuingOrg = models.CharField(max_length=100,default='')
    issuedDate = models.DateField(null=True,blank=True)
    expiryDate = models.DateField(null=True,blank=True)
    credentialId = models.CharField(max_length=100,blank=True,default='')
    credentialUrl = models.URLField(blank=True,default='')
    description = models.TextField(blank=True,default='')


class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='userTestimonial',default='',null=True)
    attestant = models.CharField(max_length=30,blank=True,default='')
    issuedDate = models.DateField(null=True,blank=True) #should not be a future date---->need to be validated
    services = models.CharField(max_length=150,blank=True,default='') #product/services
    designation = models.CharField(max_length=50,blank=True,default='') 
    location = models.CharField(max_length=150,blank=True,default='')
    description = models.TextField(blank=True,default='')

class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='userEducation',default='',null=True)
    institute = models.CharField(max_length=150,default='')
    degree = models.CharField(max_length=50,blank=True,default='')
    branch = models.CharField(max_length=30,blank=True,default='')
    grade = models.FloatField(blank=True)
    startDate = models.DateField(null=True,blank=True)
    endDate = models.DateField(null=True,blank=True)
    description = models.TextField(blank=True,default='')
