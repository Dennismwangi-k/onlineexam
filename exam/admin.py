from django.contrib import admin

# Register your models here.

from .models import ExamUser, Courses, Questions, QuestionAnswers

admin.site.register(ExamUser)
admin.site.register(Courses)
admin.site.register(Questions)
admin.site.register(QuestionAnswers)
