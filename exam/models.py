from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser
'''import abstractuser'''



# Create your models here.
class ExamUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=144, blank=True, null=True)
    last_name = models.CharField(max_length=144, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles", null=True, blank=True, default='default.png')
    phone = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        validators=[MinLengthValidator(10), MaxLengthValidator(13)],
    )

    def __str__(self):
        return self.username
    


class Courses(models.Model):
    course_name = models.CharField(max_length=50)
    course_description = models.TextField()

    def __str__(self):
        return self.course_name
    
    
class Questions(models.Model):
    QUESTION_TYPE_CHOICES = [
        ("Multiple Choice", 'Multiple Choice'),
        ("Short Answer", 'Short Answer'),
        ("True/False", 'True/False'),
    ]
    question_text = models.CharField(max_length=100)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    answer_explanation = models.TextField()
    exam = models.ForeignKey("Exam", on_delete=models.CASCADE , null=True, blank=True)


    def __str__(self):
        return self.question_text
    
class QuestionAnswers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class Exam(models.Model):
    DURATION_CHOICES = [
        ('30', '30 minutes'),
        ('60', '1 hour'),
        ('90', '1 hour 30 minutes'),
        ('120', '2 hours'),
    ]

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES)

    def __str__(self):
        return self.exam_name


class Notes(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
