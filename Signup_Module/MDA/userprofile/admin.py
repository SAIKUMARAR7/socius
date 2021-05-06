from django.contrib import admin
from .models import Profile,profilePic,Skills,Speciality,Certificate,Testimonial,Education
# Register your models here.
admin.site.register(Profile)
admin.site.register(profilePic)
admin.site.register(Skills)
admin.site.register(Speciality)
admin.site.register(Certificate)
admin.site.register(Testimonial)
admin.site.register(Education)