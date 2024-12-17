from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from accounts.models import Profile

UserModel = get_user_model()

class CreateUserForm(auth_forms.UserCreationForm):
    age = forms.IntegerField()
    # Other fields of `Profile`

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)
        # fields = auth_forms.UserCreationForm.Meta.fields + ("age",)

    #To create profile when i create user
    # def save(self, commit=True):
    #     user = super().save(commit=commit)
    #
    #     profile = Profile(
    #         user=user,
    #         age=self.cleaned_data["age"],
    #     )
    #
    #     if commit:
    #         profile.save()
    #
    #     return user
