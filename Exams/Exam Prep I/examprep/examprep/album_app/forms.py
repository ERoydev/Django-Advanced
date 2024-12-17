from django import forms
from .models import Album


class AlbumBaseForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['owner']

        widgets = {
            "album_name": forms.TextInput(attrs={'placeholder': 'Album Name'}),
            'artist': forms.TextInput(attrs={'placeholder': 'Artist'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description'}),
            'image_url': forms.TextInput(attrs={'placeholder': 'Image URL'}),
            'price': forms.TextInput(attrs={'placeholder': 'Price'}),
        }


class AddAlbumForm(AlbumBaseForm):
    pass


class EditAlbumForm(AlbumBaseForm):
    pass


class DeleteAlbumForm(AlbumBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True