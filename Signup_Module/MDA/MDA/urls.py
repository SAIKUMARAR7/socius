"""MDA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from socius import views as v
from Coupons import views as vc
from directory import views as vd
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from events import views as ve
from userprofile import views as vu
from main.views import homeFeedView, testView, leaderboardView
from pages.views import aboutPageView, searchView
from questions.views import (questionView, newView, answerView,
                            myQuestionsView, myAnswersView, questionVoteView,
                            answerVoteView)
#from markattendance import views
from rest_framework.urlpatterns import format_suffix_patterns
import quiz.views as quiz_views
import markattendance.views as mark_views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', v.index1, name="index1"),
    path('index1.html', v.index1, name="index1"),
    path('loggedin.html', v.loggedin, name="loggedin"),
    path('user.html', vu.profile, name="profile"),
    path('dashboard.html', v.dashboard, name="dashboard"),
    path('dummy.html', v.dummy, name="dummy"),
    path('directorypage.html', v.directorypage, name="directorypage"),
    path('notes',v.notes,name="notes"),
    path('team', v.Team, name="team"),
    path('about', v.About, name="About"),
    path('contact', v.contact, name="contact"),
    path('create', v.create, name="create"),
    path('alldirectories', v.alldirectories, name="alldirectories"),
    path('remove', v.remove, name="remove"),
    #path('coupons/superuser_couponcode/create', v.create, name="create"),
    path('members',v.members,name="members"),
    path('joined',v.joined,name="joined"),
    path('joindirectory',v.joindirectory,name="joindirectory"),
    path('accounts/',include('accounts.urls')),
    path('coupons/',include('Coupons.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('adduser/',v.simple_upload,name='simple_upload'),
    path('active/<uidb64>/<token>/',v.active, name='active'),
    path('activatemember/<uidb64>/<token>/<DirectoryId>/',v.activatemember, name='activatemember'),

    path('createEvent', ve.createEvent ,name="createEvent"),
    path('eventTable', ve.events_table, name="eventTable"),

    path('',include('userprofile.urls')),
    path('user.html',vu.profile,name="profile"),
    #discussion forums
    path('Discuss/', homeFeedView),
    path('test/', testView),
    path('leaderboard/', leaderboardView),
    path('searchforum/', searchView, name='search'),
    path('aboutforum/', aboutPageView),
    path('accountsforum/', include('allauth.urls')),
    path('question/<int:id>/', questionView),
    path('question/<int:id>/vote', questionVoteView),
    path('answer/<int:id>/vote', answerVoteView),
    path('question/<int:id>/answer', answerView),
    path('question/new/', newView),
    path('question/my_answers/', myAnswersView, name='my-answers'),
    path('question/my_questions/', myQuestionsView, name='my-questions'),
    #path('Nope',views.indexatten,name='Nope'),
    #path('capture', views.capture, name='capture'),
    #path("capturephoto",views.capturephoto , name="capturephoto"),
    #path("fun",views.fun , name="fun"),
    path('exam', quiz_views.exam, name="exam"),
    #proctoring
    path('proctoring/',include('proctoring.urls')),
    path('Nope', quiz_views.examindex),
	path('answer',quiz_views.answer),
	path('done',quiz_views.examquestions),
	path('createquiz',quiz_views.createquiz),
	path('availablequiz',quiz_views.availableQuizes),
    path('mark',mark_views.markindex,name='markindex'),
    path('capture', mark_views.capture, name='capture'),
    path("capturephoto",mark_views.capturephoto , name="capturephoto"),
]


urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

