from django.shortcuts import render,HttpResponse,redirect
from quiz.models import Quiz,Quizname
from socius.models import memberdirectory,DirectoryMembers
def examindex(request):
	return render(request, 'examindex.html')
def answer(request):
	questions = Quiz.objects.all()
	return render(request, 'answer.html', { 'questions': questions})
def examquestions(request):
	if request.method=='POST':
		name=request.POST['name']
		directory=request.POST['Directory']
		question_paper = request.FILES['file']
		vaildfrom=request.POST['date1']
		vaildto=request.POST['date2']
		directoryId1=memberdirectory.objects.filter(DirectoryName=directory).values('DirectoryId').first()
		directoryId=directoryId1['DirectoryId']
		optionlist=[]
		question=[]
		question_number=[]
		Final_question=[]
		content=question_paper.readlines()
		for i in range(0,len(content),6):
			li=[]
			for j in range(i,i+6):
				#f=content[j].remove("b'")
				#li.append(content[j][2:-4])
				b=(content[j].decode('utf-8'))
				#li.append(content[j][:-1])
				li.append(b[:-2])
			#print(li)
			question.append(li[0])
			li.pop(0)
			optionlist.append(li)
			
		for i in question:
			question_number.append(int(i[0]))
			Final_question.append(i[2:-1])
		#qno=['1','2']
		#Final_question=['what is your name','how are u']
		#options=[['sai','krishna','joseph','nirmal','sai'],['fine','gud','great','bad','great']]
		for i in range(len(Final_question)):
			Q=Final_question[i]
			no=question_number[i]
			opt1=optionlist[i][0]
			opt2=optionlist[i][1]
			opt3=optionlist[i][2]
			opt4=optionlist[i][3]
			opt5=optionlist[i][4]
			obj1=Quiz(name=name,DirectoryId=directoryId,qno=no,question=Q,option1=opt1,option2=opt2,option3=opt3,option4=opt4,answer=opt5)
			obj1.save()
		obj2=Quizname(name=name,DirectoryId=directoryId,vaildfrom=vaildfrom,vaildto=vaildto)
		obj2.save()
		return redirect('exam')
def createquiz(request):
	return render(request,'create quiz.html')
def availableQuizes(request):
	id=request.user.id
	user=request.user
	user1=memberdirectory.objects.filter(user_id=id).values('DirectoryId')
	user2=DirectoryMembers.objects.filter(user_id=id).values('DirectoryId')
	l=[]
	for i in range(len(user1)):
		l.append(user1[i]['DirectoryId'])
	for i in range(len(user2)):
		l.append(user2[i]['DirectoryId'])
	Quizes=[]
	q=[]
	for i in range(len(l)):
		k=Quizname.objects.filter(DirectoryId=l[i]).values('name').first()
		if k!=None:
			Quizes.append(k['name'])
	print(Quizes)
	
	return render(request,'quiz/quizname.html',{'quizes':Quizes})
def exam(request):
	id=request.user.id
	user=request.user
	user1=memberdirectory.objects.filter(user_id=id)
	return render(request,"quiz/exam.html",{'user1':user1})