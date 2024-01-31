from django.contrib import admin

from .models import Courses, ExamUser, QuestionAnswers, Questions

# Register your models here.


@admin.register(ExamUser)
class ExamUserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "username", "phone"]

admin.site.register(Courses)
admin.site.register(Questions)
admin.site.register(QuestionAnswers)
