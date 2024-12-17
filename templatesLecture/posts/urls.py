from django.urls import path
from . import views



urlpatterns = [
    path('', views.DashboardView.as_view(), name='show_posts'),
    path('add_post/', views.AddPost.as_view(), name='add_post'),
    path('edit_post/<int:pk>/', views.EditPostView.as_view(), name='edit_post'),
    path('delete_post/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('details/<int:pk>/', views.DetailPostView.as_view(), name='details_post'),
    path('search/', views.search, name='search'),

    path('approve/<int:pk>/', views.ApprovePostView.as_view(), name='approve_post'),
    # path('index/', views.IndexView.as_view(), name='index')
]
