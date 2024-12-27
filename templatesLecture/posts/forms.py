from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from .mixins import DisableFieldsMixin
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
# Pisha go taka i preizpolzvam logikata napisana v modelite


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content')

        labels = {
            'author': '',
            'content': '',
        }

        widgets = {
            "author": forms.TextInput(attrs={'placeholder': 'Your name'}),
            "content": forms.TextInput(attrs={'placeholder': 'Content here...'})
        }

    # Some stilization i could do it with widgets but here is example with init
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['author'].widgets.attr.update({
    #         'class': 'form-control',
    #         'placeholder': 'Your name',
    #     })
    #
    #     self.fields['content'].widgets.attr.update({
    #         'class': 'form-control',
    #         'placeholder': 'Content here...',
    #     })


# CommentFormSet = formset_factory(CommentForm, extra=3)

class PostCommentForm(CommentForm):
    pass


# Model Form
class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['approved', 'author', ]

    error_messages = { # Pri model forma taka se slagat error
        'title': { # field
            'required': "This field is required", # Type of error
            'max_length': "max_length should be 100"
        }
    }

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content and title in content:
            raise ValidationError("The post title cannot be included in post content!")

        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)
        post.title = post.title.capitalize()

        if commit:
            post.save()

        return post


# Vmesto da pisha taka
class PersonForm(forms.Form):
    STATUS_CHOICE = (
        (1, 'Draft'),
        (2, 'Published'),
        (3, 'Archived')
    )

    person_name = forms.CharField(max_length=10, label="First Name")
    age = forms.IntegerField()

    status = forms.IntegerField(
        widget=forms.Select(choices=STATUS_CHOICE)
    )


# I taka preizpolzvam logikata za da q preizpozlvam za create, edit ..
class PostCreateForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(PostBaseForm, DisableFieldsMixin):
    disabled_fields = ('title')
    pass


class PostConfirmForm(PostBaseForm):
    pass


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=True,
        max_length=10,
        error_messages={ # Taka naglasqm error messages tuk
            'required': 'Please write something',
            'max_length': 'The max length is 10'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': "Search..."
            }
        )
    )
