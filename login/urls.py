from django.urls import path
from login import views as login_views

urlpatterns = [
    path('login/', login_views.login, name='login'),
    path('logout/', login_views.logout, name='logout'),
    # path('register/', login_views.register, name='register')
]