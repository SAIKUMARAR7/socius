from django.contrib import admin
from quiz.models import Quiz,Quizname

# Register your models here.
class QuizAdmin(admin.ModelAdmin):
	list_display = ('question',)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Quizname)

