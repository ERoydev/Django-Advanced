import time
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic as views
# Create your views here.
from random import random

from web.models import Todo


class IndexRawView(views.View):

    def dispatch(self, request, *args, **kwargs):
        # check permissions of user

        if random() < 0.5:
            return HttpResponse('Method not allowed', request.method)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse('Class Based Views')

    def post(self, request):
        pass


class TodoCreateView(views.CreateView):
    """
    The idea is that i can get methods(placeholders) from the base methods.
    That way i can create some custom logic while using the already written methods
    """
    model = Todo
    fields = "__all__"
    template_name = 'web/create_todo.html'

    # Static way
    # success_url = reverse_lazy("index")

    # Dynamic way
    def get_success_url(self):
        # Taka dinamichno pri success otivam na details stranicata
        return reverse("todo_details", kwargs={"pk": self.object.pk})


    # Static way
    # form_class = TodoBaseForm
    """
    I pass my form like with these two things.
    """
    # Dynamic way
    def get_form_class(self):
        # return TodoBaseForm

        return super().get_form_class()

    def get_form(self, form_class=None):
        """
        Here i get the form using method from FormMixin
        To make some custom customization(small)
        """
        form = super().get_form(form_class=form_class)

        form.fields["deadline"].widget.attrs["type"] = "date"
        form.fields["deadline"].widget.attrs["class"] = "form-control"
        return form


class TodoDetailsView(views.DetailView):
    model = Todo
    template_name = "web/details_todo.html"

    # Taka s PK si raboti samo


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     context['todo'] = Todo.objects.all()

class IndexView(views.TemplateView):
    # static template
    template_name = 'web/index.html'

    # dynamic templates
    # def get_template_names(self):

    # 'context' with static data, i.e. no DB calls
    extra_context = {
        "title": "With extra content",
        "static_time": datetime.now()
    }

    # 'context' with dynamic data, i.e DB calls, ...
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['dynamic_time'] = datetime.now()

        context["todo_list"] = Todo.objects.all()

        return context