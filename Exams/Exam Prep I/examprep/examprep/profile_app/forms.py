from django import forms
from .models import Profile

# I create my BaseForm class

class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


# And i inherit it to create specific Form for my case following the good practices in programming
class CreateProfileForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        widgets = {
            "username": forms.TextInput(attrs={'placeholder': 'Username'}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
            "age": forms.TextInput(attrs={'placeholder': "Age"}),
        }

        labels = {
            "username": "Username",
            "email": "Email",
            "age": "Age",
        }