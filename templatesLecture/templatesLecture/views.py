from datetime import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, RedirectView

from posts.decorators import measure_execution_time
from posts.models import Post

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate

@method_decorator(measure_execution_time, name='dispatch')
class IndexView(TemplateView):
    template_name = 'home.html' # Static way
    extra_context = { # Static way
        'static_time': datetime.now()
    }

    def get_template_names(self): # Dynamic way
        if self.request.user.is_authenticated:
            return ['common/logged_in.html']
        else:
            return ['home.html']

    def get_context_data(self, **kwargs): # Dynamic way
        context = super().get_context_data(**kwargs)

        context['dynamic_time'] = datetime.now()
        return context


class MyRedirectView(RedirectView):
    url = reverse_lazy('home') # Static way

    # def get_redirect_url(self, *args, **kwargs): # Dynamic way
    #     pass