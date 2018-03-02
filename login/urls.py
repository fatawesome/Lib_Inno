from django.urls import path
from login import views as login_views
from . import views

urlpatterns = [
    path('login/', login_views.login, name='login'),
    path('users/', views.CustomUserListView.as_view(), name='users'),
    path('users/<int:pk>/', views.CustomUserDetailView.as_view(), name='customuser_detail'),
    path('users/<int:pk>/deleteuser/', views.delete_user, name='deleteuser'),
    path('users/<int:pk>/edituser/', views.edit_user, name='edituser'),
    path('logout/', login_views.logout, name='logout'),
    # path('register/', login_views.register, name='register')
]