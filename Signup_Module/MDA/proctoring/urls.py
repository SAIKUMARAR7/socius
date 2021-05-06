from django.contrib import admin
from django.urls import path,include
from . import views
from .views import View
app_name = 'proctoring'
urlpatterns = [
    path('start',views.start,name='start'),
    path('proctors',views.proctors,name="proctor"),
    path('submission',views.submission,name="submission"),
    path('scores',views.scores,name="scores")
]
