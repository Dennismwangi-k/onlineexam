from django.contrib import admin

from .models import Courses, ExamUser, Notes, QuestionAnswers, Questions


@admin.register(ExamUser)
class ExamUserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "username", "phone"]

admin.site.register(Courses)
admin.site.register(Questions)
admin.site.register(QuestionAnswers)
admin.site.register(Notes)