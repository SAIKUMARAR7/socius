from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile,profilePic,Skills,Speciality,Certificate,Testimonial,Education
from .forms import ProfileForm,ProfilePicForm,SkillsForm,SpecialityForm,CertificateForm,TestimonialForm,EducationForm

def dummy(request):
    return render(request,'dummy.html')

@login_required
def profile(request,*args):
    context = {}
    p_form = ProfileForm(request.POST,instance=request.user)
    pic_form = ProfilePicForm(request.POST,request.FILES,instance=request.user)
    e_form = EducationForm(request.POST,instance=request.user)
    s_form = SkillsForm(request.POST,instance=request.user)
    spcl_form = SpecialityForm(request.POST,instance=request.user)
    c_form = CertificateForm(request.POST,instance=request.user)
    t_form = TestimonialForm(request.POST,instance=request.user)
    if request.method == 'POST':
        if 'profile_form' in request.POST and p_form.is_valid():
            user = request.user
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            email = request.POST['email']
            altEmail = request.POST['altEmail']
            phone = request.POST['phone']
            altPhone = request.POST['altPhone']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            postalCode = request.POST['postalCode']
            aboutMe = request.POST['aboutMe']
            obj = Profile(firstName=firstName, lastName=lastName,email=email,altEmail=altEmail,phone=phone,altPhone=altPhone,address=address,city=city,state=state,country=country,postalCode=postalCode,aboutMe=aboutMe,user=user)
            obj.save()
            messages.success(request, 'Profile saved Successfully!!!')
            return redirect('profile') 

        if 'ppic_form' in request.POST and pic_form.is_valid():
            user = request.user
            image = request.FILES['image']
            status = request.POST['status']
            tagLine = request.POST['tagLine']
            obj = profilePic(image=image,status=status,tagLine=tagLine,user=user)
            obj.save()
            messages.success(request, 'Profile pic saved Successfully!!!')
            return redirect('profile') 

        if 'skills_form' in request.POST and s_form.is_valid():
            userSkills = request.user
            skill = request.POST['skill']
            obj = Skills(skill=skill, user=userSkills)
            obj.save()
            messages.success(request, 'Skills saved Successfully!!!')
            return redirect('profile') 

        if 'education_form' in request.POST and e_form.is_valid():
            userEducation = request.user
            institute = request.POST['institute']
            degree = request.POST['degree']
            branch = request.POST['branch']
            grade = request.POST['grade']
            startDate = request.POST['startDate']
            endDate = request.POST['endDate']
            description = request.POST['description']
            obj = Education(institute=institute,degree=degree,branch=branch,grade=grade,startDate=startDate,endDate=endDate,description=description,user=userEducation)
            obj.save()
            return redirect('profile') 

        if 'speciality_form' in request.POST and spcl_form.is_valid():
            userSpeciality = request.user
            speciality = request.POST['speciality']
            obj = Speciality(speciality=speciality, user=userSpeciality)
            obj.save()
            messages.success(request, 'Specialities saved Successfully!!!')
            return redirect('profile') 


        if 'certificate_form' in request.POST and c_form.is_valid():
            userCertificate = request.user
            name = request.POST['name']
            issuingOrg = request.POST['issuingOrg']
            issuedDate = request.POST['issuedDate']
            expiryDate = request.POST['expiryDate']
            credentialId = request.POST['credentialId']
            credentialUrl = request.POST['credentialUrl']
            description = request.POST['description']
            obj = Certificate(name=name,issuingOrg=issuingOrg,issuedDate=issuedDate,expiryDate=expiryDate,credentialId=credentialId,credentialUrl=credentialUrl,description=description,user=userCertificate)
            obj.save()
            messages.success(request, 'Certifications saved Successfully!!!')
            return redirect('profile') 
            


        if 'test_form' in request.POST and t_form.is_valid():
            userTestimonial = request.user 
            attestant = request.POST['attestant']
            issuedDate = request.POST['issuedDate']
            services = request.POST['services']
            designation = request.POST['designation']
            location = request.POST['location']
            description = request.POST['description']
            obj = Testimonial(attestant=attestant,issuedDate=issuedDate,services=services,designation=designation,location=location,description=description,user=userTestimonial)
            obj.save()
            messages.success(request, 'Testimonials saved Successfully!!!')
            return redirect('profile') 

    else:
        p_form = ProfileForm(instance=request.user)
        e_form = EducationForm(instance=request.user)
        s_form = SkillsForm(instance=request.user)
        spcl_form = SpecialityForm(instance=request.user)
        c_form = CertificateForm(instance=request.user)
        t_form = TestimonialForm(instance=request.user)
        pic_form = ProfilePicForm(instance=request.user)
    p_data = Profile.objects.all().filter(user_id=request.user.id)
    pic_data = profilePic.objects.all().filter(user_id=request.user.id)
    e_data = Education.objects.all().filter(user_id=request.user.id)
    s_data = Skills.objects.all().filter(user_id=request.user.id)
    spcl_data = Speciality.objects.all().filter(user_id=request.user.id)
    c_data = Certificate.objects.all().filter(user_id=request.user.id)
    t_data = Testimonial.objects.all().filter(user_id=request.user.id)
    context = {
        'p_form': p_form,
        'pic_form': pic_form,
        'e_form': e_form,
        's_form': s_form,
        'spcl_form': spcl_form,
        'c_form':c_form,
        't_form':t_form,
        'p_data':p_data,
        'e_data':e_data,
        'p_data': p_data,
        'pic_data':pic_data,
        'e_data': e_data,
        's_data': s_data,
        'spcl_data':spcl_data,
        'c_data':c_data,
        't_data':t_data
    }
    return render(request, 'user.html', context)


def profileUpdate(request, id): 
    context ={} 
    obj = get_object_or_404(Profile, id = id) 
    form = ProfileForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return HttpResponseRedirect("/"+id+"/profileUpdate") 
    context["form"] = form  
    return render(request, "profileUpdate.html", context) 

def skillsUpdate(request, id): 
    context ={} 
    obj = get_object_or_404(Skills, id = id) 
    form = SkillsForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return HttpResponseRedirect("/"+id+"/skillsUpdate") 
    context["form"] = form  
    return render(request, "skillsUpdate.html", context) 


def specialityUpdate(request, id): 
    context ={} 
    obj = get_object_or_404(Speciality, id = id) 
    form = SpecialityForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return HttpResponseRedirect("/"+id+"/specialityUpdate") 
    context["form"] = form  
    return render(request, "specialityUpdate.html", context) 

def certificateUpdate(request, id): 
    context ={} 
    obj = get_object_or_404(Certificate, id = id) 
    form = CertificateForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return HttpResponseRedirect("/"+id+"/certificateUpdate") 
    context["form"] = form  
    return render(request, "certificateUpdate.html", context) 

def educationUpdate(request, id): 
    context ={} 
    obj = get_object_or_404(Education, id = id) 
    form = EducationForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return HttpResponseRedirect("/"+id+"/educationUpdate") 
    context["form"] = form  
    return render(request, "educationUpdate.html", context) 

def testimonialUpdate(request, id): 
    context ={} 
    obj = get_object_or_404(Testimonial, id = id) 
    form = TestimonialForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return HttpResponseRedirect("/"+id+"/testimonialUpdate") 
    context["form"] = form  
    return render(request, "testimonialUpdate.html", context) 

def profilePicUpdate(request, id): 
    context ={} 
    obj = get_object_or_404(profilePic, id = id) 
    form = ProfilePicForm(request.POST or None, request.FILES or None,instance = obj) 
    if form.is_valid(): 
        form.save() 
        return HttpResponseRedirect("/"+id+"/profilePicUpdate") 
    context["form"] = form 
    return render(request, "profilePicUpdate.html", context) 