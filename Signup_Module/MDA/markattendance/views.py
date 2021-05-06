from django.shortcuts import render, redirect
from django.conf import settings
from io import BytesIO
from PIL import Image
import base64
import re
import face_recognition
import cv2
import os
from datetime import datetime
from csv import DictReader,writer,reader
from django.http import JsonResponse,HttpResponse
import glob
from userprofile.models import profilePic
from django.contrib.auth.decorators import login_required
name = str()
def markindex(request):
    if request.method=="POST":
        Quizname=request.POST['Quizname']
    return render(request,"attendance.html",{"Quizname":Quizname})
def capture(request):
    if request.method=="POST":
        Quizname=request.POST['Quizname']
        return render(request, 'detect.html',{"Quizname":Quizname})  

def capturephoto(request):
     if request.method == "POST":
        Quizname=request.POST['Quizname']
        img_data = request.POST.get('captured-image')
        name = request.POST.get("username")
        img_data = re.sub("^data:image/png;base64,", "", img_data)
        img_data = base64.b64decode(img_data)
        img_data = BytesIO(img_data)
       
        filename = name+'.jpg'
        image = Image.open(img_data)
        rgb_convert = image.convert("RGB")
        #print("Saved in database")###
        imgurl = "C:/Users/Sangeetha R/Desktop/attendance/photoUser/"+filename
        rgb_convert.save(imgurl)
        check_face = face_recognition.load_image_file(imgurl)
        face_location = face_recognition.face_locations(check_face)
        if len(face_location)>=1:
            print("face detected")
            result = recognize(imgurl,filename,request)
            decision =  result.pop()
            if decision:
                markattendance(name,Quizname)
                msg = name
                return render(request,'instruction.html',{"msg":msg,"Quizname":Quizname})
            else:
                msg = "Your are not in our database"
                return render(request,'detect.html',{"msg":msg})
        else:
            return render(request, 'detect.html',{"msg":"Face unable to detect.please come close to camera"})

def recognize(imgurl,filename,request):
    user = request.user.id
    a=profilePic.objects.filter(user_id=user).values('image').first()
    pathdb="C:/Users/Sangeetha R/Desktop/socius/Socius/Signup_Module/MDA/media/"+a['image']
    #pathdb = "C:/Users/Sangeetha R/Desktop/attendance/photodb/"+filename 
    User = face_recognition.load_image_file(imgurl)
    User = cv2.cvtColor(User,cv2.COLOR_BGR2RGB)

    Db = face_recognition.load_image_file(pathdb)
    Db = cv2.cvtColor(Db,cv2.COLOR_BGR2RGB)

    faceloc = face_recognition.face_locations(User)[0]
    encodeUser =  face_recognition.face_encodings(User)[0]
    cv2.rectangle(User,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)

    faceloctest = face_recognition.face_locations(Db)[0]
    encodetest =  face_recognition.face_encodings(Db)[0]
    cv2.rectangle(Db,(faceloctest[3],faceloctest[0]),(faceloctest[1],faceloctest[2]),(255,0,255),2)

    result = face_recognition.compare_faces([encodeUser],encodetest)   
    return(result)


def markattendance(name,Quiz):
    if os.path.exists(str(Quiz)+'attendance'+'.csv'):
        with open(str(Quiz)+'attendance'+'.csv',"r+") as f:
            mydatalist = DictReader(f)
            write = writer(f)
            namelist = []
            for line in mydatalist:
                namelist.append(line["Name"])
            if name not in namelist:
                now = datetime.now()
                dtstring = now.strftime("%H:%M")
                f.writelines(f'\n{name},{dtstring}')

            remove_blank_row(f)
    else:
        with open(str(Quiz)+'attendance'+'.csv',"w+") as new_file:
            columnName = ["Name","Time"]
            write = writer(new_file)
            write.writerow(columnName)
            now = datetime.now()
            dateString = now.strftime("%H:%M")
            mydata = [name,dateString]

            print("New Attendance created\n")

            #entry
           
            write.writerow(mydata)

            remove_blank_row(new_file)


def remove_blank_row(new_file):
    write=writer(new_file)
    for row in reader(new_file):
        if row:
            write.writerow(row)


def uploadQuestion(request):
    return render(request,"uploadquestion.html")


        
def question_paper_progress(request):
    
    question = []
    question_number=[]
    
    options = []
    
    answer = []
    final_option =[]
    
    if request.method == "POST":
        file = request.FILES["questionpaper"]
        #f = open(file, "r")
        content = file.readlines()
        li = []
        #print(content)
        for i in content:
            j=i.decode("UTF-8")
            li.append(j)
        
        for k in range(0,len(li),6):
            #print(k)
            question_number.append(li[k][0]) 
            question.append(li[k][2:])
            for j in range(k+1,k+6):
                options.append(li[j])
       
        
        for op in range(len(options)):
            if op%4==0 and op !=0:
                answer.append(options[op])
                
                options.pop(op)
        #
        for i in range(0,len(options),4):
            
            final_option.append(options[i:i+4])
        # print(question_number)
        # print(question)

        # print(answer)
        # print(final_option)
        
        
        
        
 


        return HttpResponse([question_number,question,final_option,answer])

#
        



