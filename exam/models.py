from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser
'''import abstractuser'''



# Create your models here.
class ExamUser(AbstractUser):
    username = models.CharField(max_length=10, primary_key=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=144, blank=True, null=True)
    last_name = models.CharField(max_length=144, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles", null=True, blank=True)
    phone = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        validators=[MinLengthValidator(10), MaxLengthValidator(13)],
    )

    def __str__(self):
        return self.username
    


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
    answer_explanation = models.TextField()
    exam_id = models.ForeignKey("Exam", on_delete=models.CASCADE , null=True, blank=True)


    def __str__(self):
        return self.question_id
    
class QuestionAnswers(models.Model):
    answer_id = models.CharField(max_length=10, primary_key=True)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_id


class Exam(models.Model):
    DURATION_CHOICES = [
        ('30', '30 minutes'),
        ('60', '1 hour'),
        ('90', '1 hour 30 minutes'),
        ('120', '2 hours'),
    ]

    exam_id = models.CharField(max_length=10, primary_key=True)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES)

    def __str__(self):
        return self.exam_id