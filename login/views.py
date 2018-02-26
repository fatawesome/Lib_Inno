from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserListView(generic.ListView):
    """
    Generic class-based view listing all users in the system.
    """
    model = CustomUser
    paginate_by = 20

class UserDetailView(generic.DetailView):
    """
    Generic class-based view the particular user.
    """
    model = CustomUser

def delete_user(request, email):
    user = CustomUser.objects.get(email=email)
    user.delete_user()
    return HttpResponseRedirect('../')


def login(request):
    """
    Login view.
    :param request: HTTP request.
    :return: login.html rendered with given context.
    """
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            login_error = "User doesn't exist"
            context = {'login_error': login_error}
            return render(request, 'login.html', context)

    else:
        return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
