from django.shortcuts import render, redirect
from .models import Profile
from ..views import get_profile


# Create your views here.


def details(request):
    profile = get_profile()
    # total_albums = len(profile.albums.all()) I do this inside html with template filter


    context = {
        'profile': profile
    }
    return render(request, 'profile-details.html', context)


def delete(request):
    profile = get_profile()

    if request.method == "POST":
        profile.delete()
        return redirect('homepage')

    context = {
        'profile': profile
    }
    return render(request, 'profile-delete.html', context)