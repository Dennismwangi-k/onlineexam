from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator


class User(AbstractUser):
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
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username