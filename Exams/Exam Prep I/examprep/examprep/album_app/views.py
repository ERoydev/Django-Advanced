from django.shortcuts import render, redirect
from .models import Album
from .forms import AddAlbumForm, EditAlbumForm, DeleteAlbumForm
from ..views import get_profile


# Create your views here.
def get_album(pk):
    return Album.objects.get(pk=pk)

def add_album(request):
    form = AddAlbumForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            profile = get_profile()
            new_album = {**form.cleaned_data, 'owner': profile}
            Album.objects.create(**new_album)
            return redirect('homepage')

    context = {
        "form": form
    }
    return render(request, 'album-add.html', context)


def details_album(request, pk):
    album = get_album(pk)

    context = {
        "album": album
    }


    return render(request, 'album-details.html', context)


def edit_album(request, pk):
    album = get_album(pk)
    profile = get_profile()

    if request.method == "POST":
        form = EditAlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = EditAlbumForm(instance=album)

    context = {
        "form": form,
        "album_pk": album.pk
    }

    return render(request, 'album-edit.html', context)


def delete_album(request, pk):
    album = get_album(pk)

    if request.method == "POST":
        album.delete()
        return redirect('homepage')

    else:
        form = DeleteAlbumForm(instance=album)


    context = {
        "form": form,
        "album_pk": album.pk,
    }

    return render(request, 'album-delete.html', context)