from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .froms import UserProfileForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
# Create your views here.
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active==True:
            auth.login(request, user)
            return redirect("loggedin")
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    else:
        context = {}

        return render(request, 'accounts/login.html',context)

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        profile_form = UserProfileForm(request.POST)
        

        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'The UserName is already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'The Email is already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.is_active=False
                #group = Group.objects.get(name='admin')
                #user.groups.add(group)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save() 
                #print('User created')
                #return redirect('login')
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = request.POST['email']
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')

        else:
            messages.info(request, 'Password Mismatch')
            return redirect('register')
        return redirect('/')


    else:
        profile_form = UserProfileForm()
        context = {'profile_form':profile_form}
        return render(request, 'accounts/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        #profile = profile_form.save(commit=False)
        #profile.user = user  
        #profile.save()
        #if user.is_active==True:
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


