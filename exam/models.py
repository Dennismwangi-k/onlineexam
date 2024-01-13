from django.db import models
from django.contrib.auth.models import AbstractUser
'''import abstractuser'''



# Create your models here.
class ExamUser(AbstractUser):
    username = models.CharField(max_length=10, primary_key=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    


class Courses(models.Model):
    user = models.ForeignKey(ExamUser, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=50)
    course_description = models.CharField(max_length=100)

    def __str__(self):
        return self.course_id
    
class Questions(models.Model):
    question_id = models.CharField(max_length=10, primary_key=True)
    question_text = models.CharField(max_length=100)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10)


    def __str__(self):
        return self.question_id
    
class QuestionAnswers(models.Model):
    answer_id = models.CharField(max_length=10, primary_key=True)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_id