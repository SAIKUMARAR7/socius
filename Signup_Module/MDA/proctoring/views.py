from django.shortcuts import render,redirect
from django.views.generic import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from io import BytesIO
from PIL import Image
import base64
import re,os,time
from django.http import JsonResponse,HttpResponse 
import face_recognition
import  cv2
import numpy as np
import dlib
from math import hypot
import random 
from csv import DictReader,writer,reader
from markattendance import views
from quiz.models import Quiz,Quizname
info = {'Center': 1, 'Left': 1, 'Right': 1, None: 1,'Mouth Open':0}
quizname = ""
Final = str()
@csrf_exempt
def start(request):
    if request.method=='POST':
        quizname=request.POST['Quizname']
        print(quizname)
        questions = Quiz.objects.filter(name=quizname)
        return render(request, 'proctor/proctor.html', { 'questions': questions,"Quizname":quizname})
@csrf_exempt
def proctors(request):
    if request.method=="POST":
        image = request.POST.get('photo',False)
        n=random.random()
        if image is not False:
            img_data = re.sub("^data:image/png;base64,", "", image)
            img_data = base64.b64decode(img_data)
            img_data = BytesIO(img_data)
            filename = time.strftime("%Y%m%d-%H%M%S")+".jpg"
            image = Image.open(img_data)
            rgb_convert = image.convert("RGB")
            imgurl = settings.MEDIA_ROOT+"/"+"attendance"+"/"+"photoUser"+"/"+filename
            rgb_convert.save(imgurl)
            instruction = proctormessage()
            msg=''
            msgpredict = []
            for key,value in instruction.items():
                if value>0 and value%5 == 0:
                    msgpredict.append(key)
                    k = msgpredict.pop()
                    if k == 'Unable to detect face':
                        msg = 'Unable to detect face'
                        return HttpResponse({msg}, status=200)
                    elif k == "Left" or k == "Right":
                        msg = "Don't look away from test screen"
                       # print(msg)
                        return HttpResponse({msg}, status=200)
                    elif k == 'None':
                        msg = "Don't move your head fastly"
                        return HttpResponse({msg}, status=200)
                    elif k == "Mouth Open":
                        msg = "Don't speak or open your open your mouth"
                        return HttpResponse({msg},status=200)
                    else:
                        msg = ''
                        return HttpResponse({msg}, status=200)
            #print(instruction)
            return HttpResponse({msg}, status=200)
      
   

def proctormessage():
    path='E:/attendance/photoUser'
    
    for i in os.listdir(path):
        if i.endswith(".jpg"):
            
            msg=proctoroperation(path+'/'+i)
            if msg in info.keys():
                info[msg] += 1
                print(info)
                try:
                    os.remove(path+"/"+i)
                    return info
                except:
                    pass                

            else:
                
                info[msg] = 0
                try:
                    os.remove(path+"/"+i)
                    return info
                except:
                    pass
                    
def proctoroperation(imgurl):
    
    cap = cv2.imread(imgurl)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('F:/attendance/proctoring/shape_predictor_68_face_landmarks.dat')
       
    try:
        #print("in try")
        gray = cv2.cvtColor(cap,cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
        
            landmarks = predictor(gray, face)
#Blink detection
            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
            
            if blinking_ratio>4:
                return "Center"
                #return blinking_ratio
            
            gaze_ratio_left = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks,cap,gray)
            gaze_ratio_right = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks,cap,gray)
            gaze_ratio = (gaze_ratio_right+gaze_ratio_left)/2
            #return gaze_ratio

            center_top_mouth = (landmarks.part(63).x, landmarks.part(63).y)
            center_bottom_mouth = (landmarks.part(65).x, landmarks.part(65).y)
            
            
            
            ver_line_length = hypot((center_top_mouth[0]-center_bottom_mouth[0]),(center_top_mouth[1]-center_bottom_mouth[1]))
            #hor_line_length = hypot(()-())
            
            if ver_line_length > 5:
               return("Mouth Open")
            if gaze_ratio<0.40:
                return 'Right'
            elif gaze_ratio>0.40 and gaze_ratio<1.3:
                return 'Center'
            elif gaze_ratio>1.6 and gaze_ratio<4:
                return 'Left'
    except:
        return "Unable to detect face"
        #pass

def get_blinking_ratio(eye_points, facial_landmarks):
    
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    
    ratio = hor_line_lenght / ver_line_lenght
    return ratio

def get_gaze_ratio(eye_points,facial_landmarks,cap,gray):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                            (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                            (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                            (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                            (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                            (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

        
    height, width, _ = cap.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    left_eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])
    

    gray_eye = left_eye[min_y: max_y, min_x: max_x]

    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)

    height , width =threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)
   # print(right_side_white)

    
    if left_side_white == 0:
        gaze_ratio = 3
    elif right_side_white == 0:
        gaze_ratio = 0.001
    try:
        gaze_ratio = left_side_white / right_side_white
    except:
        gaze_ratio = 0.50

    return gaze_ratio

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

# @csrf_exempt    
def submission(request):
    #get user name here from database
    #get quizname from database
    name= request.user
    #quizname = "django" #i don't know how to get quizname here
    if request.method=='POST':
        mark = request.POST["score"]
        quizname=request.POST['Quizname']
        #obj=Scores(score=mark)
        #obj.save()
        #print(mark)
    #print("resultinfo", info)
    
    max_val = max(info.values())
    max_pair = (tuple(k for k in info if info[k] == max_val), max_val)
    largekey = max_pair[0][0]
    
    if largekey == 'None':
        check = info["None"]-info["Center"]
        if check > 5:
            Final = "Malpractise"
        else:
            Final = "Eligble"
    elif largekey == "Right":
        Final = "Malpractise"


    # elif info["Left"]*1.5 >= info["Center"] or info['Right']*1.5>= info["Center"]:
    elif info['Right']*1.5>= info["Center"]:
        Final = "Malpractise"
        
    else:
        Final = "Eligble"
    #print(Final)
    if os.path.exists(str(quizname)+'mark'+'.csv'):
        with open(str(quizname)+'mark'+'.csv',"r+") as f:
            mydatalist = DictReader(f)
            write = writer(f)
            namelist = []
            for line in mydatalist:
                namelist.append(line["Name"])
            if name not in namelist:
                
                f.writelines(f'\n{name},{mark},{Final}')

            
    else:
        with open(str(quizname)+'mark'+'.csv',"w+") as new_file:
            columnName = ["Name","Mark","Category"]
            write = writer(new_file)
            write.writerow(columnName)
            
            mydata = [name,mark,Final]

            print("New marKlist created\n")

            #entry
           
            write.writerow(mydata)

    return render(request,'proctor/sub.html')
@csrf_exempt  
def scores(request):
    #print("In score")
    if request.method == "POST":
        result = request.POST.get('scores')

        obj=Scores(score=result)
        obj.save()
        #print("saved")

    return HttpResponse("End of exam"+ result)