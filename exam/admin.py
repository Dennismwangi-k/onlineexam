from django.contrib import admin

from .models import Courses, ExamUser, QuestionAnswers, Questions

# Register your models here.


admin.site.register(ExamUser)
admin.site.register(Courses)
admin.site.register(Questions)
admin.site.register(QuestionAnswers)
