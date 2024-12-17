
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserForm


class RegisterView(CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('home')
    form_class = CustomUserForm
