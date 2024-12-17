from django.contrib import admin
from django.contrib.auth import get_user_model

from posts.models import Post

UserModel = get_user_model()

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass