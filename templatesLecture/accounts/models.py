from django.contrib.auth.models import AbstractUser, User
from django.db import models
# Create your models here.


class CustomUser(AbstractUser):
    points = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    age = models.IntegerField()

    first_name = models.CharField(
        max_length=30,
    )

    last_name = models.CharField(
        max_length=30,
    )

    points = models.IntegerField(
        default=0
    )