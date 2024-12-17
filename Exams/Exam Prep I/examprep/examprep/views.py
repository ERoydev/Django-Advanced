from django.http import HttpResponse
from django.shortcuts import render, redirect
from examprep.profile_app.models import Profile
from examprep.profile_app.forms import CreateProfileForm

from examprep.album_app.models import Album



def get_profile():
    return Profile.objects.first()


def create_profile(form):
    form.save()


def homepage(request):
    form = CreateProfileForm(request.POST or None)
    profile = get_profile()

    if request.method == "GET":
        if profile is None:
            context = {
                "form": form,
                "has_profile": False
            }
            return render(request, 'home-no-profile.html', context)

    if request.method == "POST":
        if form.is_valid() and not profile:
            create_profile(form)

    all_albums = Album.objects.filter(owner_id=profile.pk)
    context = {
        "profile": profile,
        "has_profile": True,
        "albums": all_albums
    }

    return render(request, 'home-with-profile.html', context)
