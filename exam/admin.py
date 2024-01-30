from django.contrib import admin

# Register your models here.

from .models import ExamUser, Courses, Questions, QuestionAnswers, Notes

admin.site.register(ExamUser)
admin.site.register(Courses)
admin.site.register(Questions)
admin.site.register(QuestionAnswers)
admin.site.register(Notes)