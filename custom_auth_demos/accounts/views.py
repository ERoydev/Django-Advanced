from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as views
from .forms import CreateUserForm


class LoginUserView(auth_views.LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("index")


class RegisterUserView(views.CreateView):
    form_class = CreateUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy("index")

