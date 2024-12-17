from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_user'),
    path('login/', views.LoginView.as_view(), name='login_user'),
    path('logout/', views.LogoutView.as_view(), name='logout_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token')
]
