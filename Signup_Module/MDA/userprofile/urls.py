from django.urls import path, include
from django.contrib import admin
from . import views as v
  
urlpatterns = [ 
    path('user.html', v.profile, name="profile"),
    path('<id>/profilePicUpdate', v.profilePicUpdate,name="profilePicUpdate" ),
    path('<id>/profileUpdate', v.profileUpdate,name="profileUpdate" ), 
    path('<id>/skillsUpdate', v.skillsUpdate,name="skillsUpdate" ), 
    path('<id>/specialityUpdate', v.specialityUpdate,name="specialityUpdate" ), 
    path('<id>/educationUpdate', v.educationUpdate,name="educationUpdate" ), 
    path('<id>/certificateUpdate', v.certificateUpdate,name="certificateUpdate" ),
    path('<id>/testimonialUpdate',v.testimonialUpdate,name="testimonialUpdate")
] 
'''
urlpatterns = [
        #path('admin/', admin.site.urls),
        path('profile', views.profile,name="profile"), 
        path('dummy',views.dummy,name="dummy")
]
'''