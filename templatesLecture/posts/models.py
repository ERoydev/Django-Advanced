from django.contrib.auth import get_user_model
from django.db import models

from .validators import BadLanguageValidator

# Create your models here.

UserModel = get_user_model()


class Post(models.Model):
    LANGUAGES_CHOICES = (
        ('BG', 'Bulgarian'),
        ('EN', 'English')
    )
    title = models.CharField(
        max_length=100,
    )

    content = models.TextField(
        validators=[BadLanguageValidator]

    )

    author = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    languages = models.CharField(
        max_length=100,
        choices=LANGUAGES_CHOICES,
    )

    approved = models.BooleanField(
        default=False,
    )

    class Meta:
        permissions = [
            ('can_approve_posts', 'Can approve posts'),
        ]

    def __str__(self):
        return self.title


# class PostChild(Post):
#     pass

class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    author = models.CharField(
        max_length=100
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class CustomProxyModel(Comment):
#     age = models.IntegerField()
#
#     def custom_method(self):
#         return f"This is a custom method"
#
#     class Meta:
#         proxy = True