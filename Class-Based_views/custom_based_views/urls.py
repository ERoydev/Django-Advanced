from django.urls import path
from . import views

urlpatterns = [
    path('fbv/', views.index, name='fbv_index'),
    path('cbv/', views.IndexView.as_view(), name='cbv_index')
]
