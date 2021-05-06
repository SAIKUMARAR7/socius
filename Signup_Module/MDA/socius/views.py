from django.shortcuts import render, redirect
from .models import *
from .models import UserList , memberdirectory,DirectoryMembers
from .resources import UserListResource
from django.contrib import messages
from tablib import Dataset 
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from django.core import mail
from .forms import DirectoryCreationForm,DirectoryjoinForm
#import uuid 
#from .models import MemberProfile,Phone,Address,Speciality,KeySKills,Certificates,Testimonial,Document,AcademicDetails,Event
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, admin_only
from events.models import Event


from userprofile import models as m 
# Create your views here.
# for Html email stuff
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags 
def index1(response):
    mems = memberdirectory.objects.all()
    return render(response, "socius/index1.html", {'mems': mems})

def loggedin(request):
    id=request.user.id
    user=request.user
    user1=memberdirectory.objects.filter(user_id=id).first()
    user2=DirectoryMembers.objects.filter(user_id=id).first()
    events = Event.objects.all
    if(user1 is not None)and(user2 is None):
        l=[]
        id=request.user.id
        dir=memberdirectory.objects.filter(user_id=id).all()
        mydir1=DirectoryMembers.objects.filter(user_id=id).values('DirectoryId')
        for i in mydir1:
            l.append(i['DirectoryId'])
        #print(l)
        for j in l:
            mydir=memberdirectory.objects.filter(DirectoryId=j).all()
        return render(request,'socius/dashboard.html',{'dir':dir, 'events':events})
    elif (user1 is None)and(user2 is not None):
        l=[]
        k=[]
        mydir={}
        id=request.user.id
        mydir1=DirectoryMembers.objects.filter(user_id=id).values('DirectoryId')
        for i in mydir1:
            l.append(i['DirectoryId'])
        #print(l)
        for j in range(len(l)):
            mydir2=memberdirectory.objects.filter(DirectoryId=l[j])
            mydir.setdefault('Directory', []).append(mydir2)
        for i in range(len(l)):
            k.append(mydir['Directory'][i])
        #print(k)
        return render(request,'socius/dashboard.html',{'k':k, 'events':events})
    elif (user1 is not None)and(user2 is not None):
        if request.method == 'POST':
            #print('Enter outer IF Simple Upload')
            if 'simple_upload' in request.POST:
                user_list = UserListResource()
                dataset = Dataset()
                new_person = request.FILES['myfile']
                #print('Enter inner IF Simple Upload')

                if not new_person.name.endswith('xlsx'):
                    messages.info(request, 'Wrong Format')
                    return render(request, 'socius/upload.html')

                imported_data = dataset.load(new_person.read(),format='xlsx')
                #print(imported_data)
                d=[]
                p=[]
                for data in imported_data:
                    #print(data[1])
                    #UserListInvitation(data[2])
                    d.append(data[2])
                    p.append(data[3])
                    value = UserList(
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        
                        )
                    value.save()
                l=d
                k=p[0]
                user=User.objects.filter(is_superuser='True').first()
                current_site = get_current_site(request)
                mail_subject = 'Invite to Socius'
                message = render_to_string('socius/invite.html', {
                    'user': user,
                    'k':k,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                for i in l:
                    #reciever_list.append(i['email'])
                    to_email = i
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                return redirect('loggedin.html')
            if 'DirId' in request.POST:
                #print('inside DirId request')
                DirectoryId=request.POST['DirectoryId']
                user = request.user.id
                Email = request.user.email
                Name = request.user.username  
                if DirectoryMembers.objects.filter(Email=Email).exists():
                    messages.info(request, 'The email is already registered')
                    return redirect('dashboard')
                else:
                    obj3=DirectoryMembers(Name=Name,Email=Email,DirectoryId=DirectoryId,user_id=user)
                    obj3.save()
                    return redirect('dashboard')
        l=[]
        k=[]
        mydir={}
        id=request.user.id
        dir=memberdirectory.objects.filter(user_id=id).all()
        #print(dir)
        mydir1=DirectoryMembers.objects.filter(user_id=id).values('DirectoryId')
        for i in mydir1:
            l.append(i['DirectoryId'])
        #print(l)
        for j in range(len(l)):
            mydir2=memberdirectory.objects.filter(DirectoryId=l[j]).all()
            mydir.setdefault('Directory', []).append(mydir2)
            #print(mydir)
        for i in range(len(l)):
            k.append(mydir['Directory'][i])
        #print(k)
        current_user = request.user 
        current_user_id = current_user.id 
        createddir = memberdirectory.objects.filter(user_id=current_user_id).all()
        #print(createddir) 
        return render(request,'socius/dashboard.html',{'dir':dir,'k':k,'createddir':createddir,'events':events})


    else:
        return render(request,'socius/dashboard1.html',{'events':events})


def dashboard(request,*args):
    id=request.user.id
    user=request.user
    user1=memberdirectory.objects.filter(user_id=id).first()
    user2=DirectoryMembers.objects.filter(user_id=id).first()
    events = Event.objects.all
    
    
    if(user1 is not None)and(user2 is None):
        if request.method == 'POST':
            #print('Enter outer IF Simple Upload')
            if 'simple_upload' in request.POST:
                user_list = UserListResource()
                dataset = Dataset()
                new_person = request.FILES['myfile']
                #print('Enter inner IF Simple Upload')

                if not new_person.name.endswith('xlsx'):
                    messages.info(request, 'Wrong Format')
                    return render(request, 'socius/upload.html')

                imported_data = dataset.load(new_person.read(),format='xlsx')
                #print(imported_data)
                d=[]
                c=[]
                for data in imported_data:
                    #print(data[1])
                    #UserListInvitation(data[2])
                    d.append(data[2])
                    c.append(data[3])
                    '''send_mail(
                        'MDA Invitation',
                        'This is the Invitation of MDA applcation.',
                        settings.EMAIL_HOST_USER,
                        [data[2]],
                        fail_silently=False,
                    )'''

                    #value = UserList(
                    #    data[0],
                    #    data[1],
                    #    data[2],
                     #   data[3],
                      #  data[4]
                       # )
                    #value.save()
                
                l=d
                user=User.objects.filter(is_superuser='True').first()
                current_site = get_current_site(request)
                #mail_subject = 'Invite to Socius'
                message = render_to_string('socius/invite.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    
                })
                for i in range(len(l)):
                    #reciever_list.append(i['email'])
                    to_email = l[i]
                    email = EmailMessage(
                        'Invite to Socius'+":"+"DirectoryId "+c[i], message, to=[to_email]
                    )
                    email.send()
                return redirect('dashboard')
            if 'DirId' in request.POST:
                #print('inside DirId request')
                DirectoryId=request.POST['DirectoryId']
                #print(DirectoryId,'checking') 
                user = request.user.id
                Email = request.user.email
                Name = request.user.username  
                obj3=DirectoryMembers(Name=Name,Email=Email,DirectoryId=DirectoryId,user_id=user)
                obj3.save()
                return redirect('dashboard')
        l=[]
        id=request.user.id
        dir=memberdirectory.objects.filter(user_id=id).all()
        mydir1=DirectoryMembers.objects.filter(user_id=id).values('DirectoryId')
        for i in mydir1:
            l.append(i['DirectoryId'])
        #print(l)
        for j in l:
            mydir=memberdirectory.objects.filter(DirectoryId=j).all()
        return render(request,'socius/dashboard.html',{'dir':dir,'events':events})
    elif (user1 is None)and(user2 is not None):
        if 'DirId' in request.POST:
            #print('inside DirId request')
            DirectoryId=request.POST['DirectoryId']
            #print(DirectoryId,'checking') 
            user = request.user.id
            Email = request.user.email
            Name = request.user.username  
            obj3=DirectoryMembers(Name=Name,Email=Email,DirectoryId=DirectoryId,user_id=user)
            obj3.save()
            return redirect('dashboard')
        l=[]
        k=[]
        mydir={}
        id=request.user
        mydir1=DirectoryMembers.objects.filter(user_id=id,active=True).values('DirectoryId')
        for i in mydir1:
            l.append(i['DirectoryId'])
        #print(l)
        for j in range(len(l)):
            mydir2=memberdirectory.objects.filter(DirectoryId=l[j])
            mydir.setdefault('Directory', []).append(mydir2)
        for i in range(len(l)):
            k.append(mydir['Directory'][i])
        #print(k)
        return render(request,'socius/dashboard.html',{'k':k,'events':events})
    elif (user1 is not None)and(user2 is not None):
        if request.method == 'POST':
            #print('Enter outer IF Simple Upload')
            if 'simple_upload' in request.POST:
                user_list = UserListResource()
                dataset = Dataset()
                new_person = request.FILES['myfile']
                #print('Enter inner IF Simple Upload')

                if not new_person.name.endswith('xlsx'):
                    messages.info(request, 'Wrong Format')
                    return render(request, 'socius/upload.html')

                imported_data = dataset.load(new_person.read(),format='xlsx')
                #print(imported_data)
                d=[]
                c=[]
                for data in imported_data:
                    #print(data[1])
                    #UserListInvitation(data[2])
                    d.append(data[2])
                    c.append(data[3])
                    '''send_mail(
                        'MDA Invitation',
                        'This is the Invitation of MDA applcation.',
                        settings.EMAIL_HOST_USER,
                        [data[2]],
                        fail_silently=False,
                    )'''

                    value = UserList(
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4]
                        )
                    value.save()
                l=d
                user=User.objects.filter(is_superuser='True').first()
                current_site = get_current_site(request)
                #mail_subject = 'Invite to Socius'
                message = render_to_string('socius/invite.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    
                })
                for i in range(len(l)):
                    #reciever_list.append(i['email'])
                    to_email = l[i]
                    email = EmailMessage(
                        'Invite to Socius'+":"+"DirectoryId "+c[i], message, to=[to_email]
                    )
                    email.send()
                return redirect('dashboard')
            if 'DirId' in request.POST:
                #print('inside DirId request')
                DirectoryId=request.POST['DirectoryId']
                #print(DirectoryId,'checking') 
                user = request.user.id
                Email = request.user.email
                Name = request.user.username  
                obj3=DirectoryMembers(Name=Name,Email=Email,DirectoryId=DirectoryId,user_id=user)
                obj3.save()
                return redirect('dashboard')
        l=[]
        k=[]
        mydir={}
        id=request.user
        
        mydir1=DirectoryMembers.objects.filter(user_id=id,active=True).values('DirectoryId')
        for i in mydir1:
            l.append(i['DirectoryId'])
       
        for j in range(len(l)):
            mydir2=memberdirectory.objects.filter(DirectoryId=l[j]).all()
            mydir.setdefault('Directory', []).append(mydir2)
            #print(mydir)
        for i in range(len(l)):
            k.append(mydir['Directory'][i])
       
        current_user = request.user 
        current_user_id = current_user.id 
        createddir = memberdirectory.objects.filter(user_id=current_user_id).all()
        #print(createddir) 
        #return render(request,'socius/dashboard.html',{'dir':dir,'k':k,'createddir':createddir})
        return render(request,'socius/dashboard.html',{'dir':mydir,'k':k,'createddir':createddir,'events':events})


    else:
        if request.method == 'POST':
            if 'DirId' in request.POST:
                #print('inside DirId request')
                DirectoryId=request.POST['DirectoryId']
                #print(DirectoryId,'checking') 
                user = request.user.id
                Email = request.user.email
                Name = request.user.username  
                obj3=DirectoryMembers(Name=Name,Email=Email,DirectoryId=DirectoryId,user_id=user)
                obj3.save()
                return redirect('dashboard')
        return render(request,'socius/dashboard1.html')

def Team(request):
    return render(request, "socius/team.html")

def About(request):
    return render(request,"socius/about.html")

def contact(request):
    return render(request,"socius/contact.html")

@login_required(login_url='login')
def directorypage(request):
    if request.method=='POST':
        directoryid=request.POST['DirectoryId']
        user1=request.user.id
        superuser=memberdirectory.objects.get(DirectoryId=directoryid)
        superuserId=superuser.user_id
        Su=User.objects.get(id=superuserId)
        SuperUser=Su.username 
        #print(type(U),type(SuperUser))
        userid1=memberdirectory.objects.filter(DirectoryId=directoryid).values('user_id').first()
        userid=userid1['user_id']
        superuser=User.objects.filter(id=userid).first()
        superuserprofile = m.profilePic.objects.get(user_id=superuserId)
        SuPic = superuserprofile.image
        members=DirectoryMembers.objects.filter(DirectoryId=directoryid)
        l=[]
        mempic={}
        for i in members:
            l.append(i.user_id)
        lp=[]
        for i in l:
            s=m.profilePic.objects.filter(user_id=i)
            #mempic.setdefault('image',[]).append(s)
            lp.append(s)
        n=len(lp) 
        #admin=User.objects.filter(is_superuser='True').first()
        notes=Notes.objects.filter(DirectoryId=directoryid)
        
        context={'members':members,'SuperUser':SuperUser,'SuPic':SuPic,'lp':lp,'n':n,'superuser':superuser,'directoryid':directoryid,'user1':user1,'notes':notes}
        return render(request,'socius/directorypage.html',context)
    else:
        return redirect('loggedin')



@allowed_users(allowed_roles=['admin','superuser'])
def simple_upload(request,*args):
    if request.method == 'POST':
        user_list = UserListResource()
        dataset = Dataset()
        new_person = request.FILES['myfile']

        if not new_person.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'socius/upload.html')

        imported_data = dataset.load(new_person.read(),format='xlsx')
        #print(imported_data)
        d=[]
        for data in imported_data:
        	#print(data[1])
            #UserListInvitation(data[2])
            d.append(data[2])
            '''send_mail(
                'MDA Invitation',
                'This is the Invitation of MDA applcation.',
                settings.EMAIL_HOST_USER,
                [data[2]],
                fail_silently=False,
            )'''

            value = UserList(
        		data[0],
        		data[1],
        		 data[2],
        		 data[3],
                 data[4]
        		)
            value.save()
        l=d
        user=User.objects.filter(is_superuser='True').first()
        current_site = get_current_site(request)
        mail_subject = 'Invite to Socius'
        message = render_to_string('socius/invite.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        for i in l:
            #reciever_list.append(i['email'])
            to_email = i
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
        return HttpResponse('Invitations sended')
        '''connection = mail.get_connection()
        connection.open()
        email1 = mail.EmailMessage('MDA Invitation', 'This is the Invitation of MDA applcation.', settings.EMAIL_HOST_USER, d, connection=connection)
        email1.send()
        connection.close()'''

            
            #send_mail('Invitation MDA','This is MDA application Invitation',settings.EMAIL_HOST_USER, data[2], fail_silently=False)
            #send_mail('Invitation MDA', 'This is MDA application Invitation', settings.EMAIL_HOST_USER, data[2], fail_silently=False)
    return render(request, 'socius/upload.html')

    



def active(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
      #  user.save()
        if user.is_active==True:
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
            return redirect('register')
    else:
        return HttpResponse('Invitation link is invalid!')


def create(request,*args,**kwargs):
    if request.method=='POST':
        form=DirectoryCreationForm(request.POST,request.FILES)
        if form.is_valid():
            id=request.user.id
            user=User.objects.filter(id=id).first()
            DirectoryName=request.POST['DirectoryName']
            Description=request.POST['Description']
            img=request.FILES['img']
            DirectoryId=request.POST['DirectoryId']
            MemberLimit=request.POST['MemberLimit']
            obj1=memberdirectory(DirectoryName=DirectoryName,Description=Description,DirectoryId=DirectoryId,MemberLimit=MemberLimit,img=img,user=user)
            obj1.save()
            return redirect('dashboard')
    else:
        form=DirectoryCreationForm()
    return render(request,'socius/createdir.html',{'form':form})

def members(response):
    Members=DirectoryMembers.objects.filter()
    return render(response, "socius/Members.html",{'Members':Members})

def dummy(response):
    DirectoryId = DirectorymembersDirectory.objects.filter(memberdirectory_id=9)
    print(DirectoryId)


@login_required
def joindirectory(request):
    return render(request,'socius/joindirectory1.html')



def joind(request):
    if request.method=='POST':
        form=DirectoryjoinForm(request.POST)
        if form.is_valid():
            user=request.user.id
            Name=request.POST['Name']
            #Email=request.POST['email']
            Email=request.user.email 
            Bio=request.POST['Bio']
            DirectoryId=request.POST['DirectoryId']
            #user=User.objects.filter(is_superuser='True').first()
            #Dirctory_id=DirectoryCreation.objects.filter('id',user_id=user.id)
            if DirectoryMembers.objects.filter(Email=Email,DirectoryId=DirectoryId).exists():
                messages.info(request, 'The email is already registered')
                return redirect('joined')
            elif memberdirectory.objects.filter(DirectoryId=DirectoryId).exists():
                user1=request.user.id
                obj1=DirectoryMembers(Name=Name,Email=Email,Bio=Bio,DirectoryId=DirectoryId,user_id=user1)
                obj1.save()
                #user=User.objects.filter(id=user2).first()
                user=request.user
                superuser=memberdirectory.objects.get(DirectoryId=DirectoryId)
                superuserId=superuser.user_id
                Su=User.objects.get(id=superuserId)
                Email_id=Su.email
                sname=Su.username 
                DirectoryName=memberdirectory.objects.filter(DirectoryId=DirectoryId).values('DirectoryName').first()
                #print(DirectoryName)
                #print(Email_id)
                #Email_id=Email_idd['email']
                current_site = get_current_site(request)
                to_email=Email_id
                mail_subject = 'New member joined to directory'
                message = render_to_string('socius/joinrequest.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'sname':sname,
                    'DirectoryName':DirectoryName,
                    'DirectoryId':DirectoryId,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                #html_content = render_to_string("socius/joinrequest.html",{'sname':sname,'user1':user1,'DirectoryName':DirectoryName})
                #text_content = strip_tags(html_content)
                #email = EmailMultiAlternatives(
                #    'New member joined to directory',
                #    text_content,
                #    settings.EMAIL_HOST_USER,
                #    to_email
                #)
                
                email = EmailMessage(
                mail_subject, message, to=[to_email]
                )
                email.send()
                #return redirect('dashboard')
                return render(request,'socius/joinedresponse.html')
            else:
                return render(request,'socius/InvaildDirectoryId.html')
    else:
        form=DirectoryjoinForm()
    return render(request,'socius/joindirectory1.html',{'form':form})
def activatemember(request, uidb64, token,DirectoryId):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        obj1=DirectoryMembers.objects.filter(Name=user.username,DirectoryId=DirectoryId).first()
        obj1.active = True
        obj1.save()
        #if user.is_active==True:
        return HttpResponse('Member Added to your directory')
            #return redirect('register')
    else:
        return HttpResponse('request link is invalid!')



def remove(request,*args,**kwargs):
    if request.method=='POST':
        id1=request.POST['user_id']
        #print(id1)
        directoryid=request.POST['directoryid']
        member=DirectoryMembers.objects.filter(user_id=id1,DirectoryId=directoryid)
        member.delete()
        #return render(request,'socius/dashboard.html')
        return redirect('loggedin.html')

def alldirectories(request):
    user1 = request.user 
    mems=memberdirectory.objects.exclude(user_id=user1)
    return render(request,'socius/alldirectories.html', {'mems': mems})
def joined(request):
    if request.method=='POST':
            user=request.user.id
            Name=request.user.username
            #Email=request.POST['email']
            Bio="helo"
            Email=request.user.email 
            DirectoryId=request.POST['DirectoryId']
            #user=User.objects.filter(is_superuser='True').first()
            #Dirctory_id=DirectoryCreation.objects.filter('id',user_id=user.id)
            if DirectoryMembers.objects.filter(Email=Email,DirectoryId=DirectoryId).exists():
                messages.info(request, 'The email is already registered')
                return redirect('joined')
            elif memberdirectory.objects.filter(DirectoryId=DirectoryId).exists():
                user1=request.user.id
                obj1=DirectoryMembers(Name=Name,Email=Email,Bio=Bio,DirectoryId=DirectoryId,user_id=user1)
                obj1.save()
                #user=User.objects.filter(id=user2).first()
               
                #html_content = render_to_string("socius/joinrequest.html",{'sname':sname,'user1':user1,'DirectoryName':DirectoryName})
                #text_content = strip_tags(html_content)
                #email = EmailMultiAlternatives(
                #    'New member joined to directory',
                #    text_content,
                #    settings.EMAIL_HOST_USER,
                #    to_email
                #)
                
                
                return redirect('loggedin.html')
            else:
                return render(request,'socius/InvaildDirectoryId.html')
    
    return render(request,'socius/dashboard.html')
def notes(request):
    if request.method=='POST':
        files=request.FILES['file']
        directoryid=request.POST['directoryid']
        obj1=Notes(files=files,DirectoryId=directoryid)
        obj1.save()
        return redirect('loggedin')
        

    else:
        return render(request,'socius/directorypage.html')
