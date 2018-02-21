from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm


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
