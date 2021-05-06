from django.db import models

# Create your models here.
class Quizname(models.Model):
	name = models.CharField(max_length = 500)
	DirectoryId=models.CharField(max_length=10,default='')
	vaildfrom=models.DateField(default='2010-04-10')
	vaildto=models.DateField(default='2012-06-10')

class Quiz(models.Model):
	name = models.CharField(max_length = 500)
	DirectoryId=models.CharField(max_length=10,default='')
	qno=models.IntegerField(default=0)
	question = models.CharField(max_length = 500)
	option1 = models.CharField(max_length = 300)
	option2 = models.CharField(max_length = 300)
	option3 = models.CharField(max_length = 300)
	option4 = models.CharField(max_length = 300)
	answer = models.CharField(max_length = 300)

