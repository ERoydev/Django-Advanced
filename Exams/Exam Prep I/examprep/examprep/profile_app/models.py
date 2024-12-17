from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator


class Profile(models.Model):
    username = models.CharField(
        max_length=15,
        validators=[MinLengthValidator(2)],
        null=True,
        blank=True
    )

    email = models.EmailField(
        null=False,
        blank=False
    )

    age = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.username
