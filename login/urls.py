from django.urls import path
from login import views as login_views
from . import views

urlpatterns = [
    path('login/', login_views.login, name='login'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/(?P<email>[\w\-]+)/', views.UserDetailView.as_view(), name='customuser-detail'),
    path('users/(?P<email>[\w\-]+)/deleteuser/', views.delete_user, name='deleteuser'),
    path('logout/', login_views.logout, name='logout'),
    # path('register/', login_views.register, name='register')
]