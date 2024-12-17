from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('initkwargs/', TemplateView.as_view(template_name='web/index.html')),
    path('raw/', views.IndexRawView.as_view(), name='index_raw'),
    path('todos/create', views.TodoCreateView.as_view(), name="todo_create"),
    path('todos/<int:pk>/', views.TodoDetailsView.as_view(), name="todo_details")
]
