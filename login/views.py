from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.contrib.auth.models import Group


class CustomUserListView(generic.ListView):
    """
    Generic class-based view listing all users in the system.
    """
    model = CustomUser


class CustomUserDetailView(generic.DetailView):
    """
    Generic class-based view the particular user.
    """
    model = CustomUser

@permission_required('login.delete_customuser')
def delete_user(request, pk):
    """
    Delete user from the system.
    :param request: HTTP request.
    :param pk: user id.
    :return: HTTP redirect to user page.
    """
    user = CustomUser.objects.get(pk=pk)
    user.delete_user()
    return HttpResponseRedirect(reverse('users'))


def get_or_create_group(name):
    if Group.objects.filter(name=name).count() != 0:
        return Group.objects.get(name=name)
    group = Group.objects.create(name=name)
    return group


@permission_required('login.change_customuser')
def edit_user(request, pk):
    """
    View function for editing a user.
    :param request: HTTP request.
    :param pk: user id.
    :return: rendered edit_user page.
    """
    user = CustomUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user, caller_is_admin=request.user.is_admin)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.address = form.cleaned_data['address']
            user.subtype = form.cleaned_data['subtype']

            for queue_elem in user.requestqueueelement_set.all():
                queue_elem.priority = queue_elem.default_priority()
                queue_elem.save()

            user.groups.clear()
            if form.cleaned_data['subtype'] == 'Librarians (Priv1)':
                user.groups.add(get_or_create_group(name='Librarians (Priv1)'))
            elif form.cleaned_data['subtype'] == 'Librarians (Priv2)':
                user.groups.add(get_or_create_group(name='Librarians (Priv2)'))
            elif form.cleaned_data['subtype'] == 'Librarians (Priv3)':
                user.groups.add(get_or_create_group(name='Librarians (Priv3)'))
            elif form.cleaned_data['subtype'] == 'Students':
                user.groups.add(get_or_create_group(name='Students'))
            elif form.cleaned_data['subtype'] == 'Visiting Professors':
                user.groups.add(get_or_create_group(name='Visiting Professors'))
            else:  # if self.cleaned_data['subtype'] equal 'Instructors' or 'TAs' or 'Professors'
                user.groups.add(get_or_create_group(name='Faculty'))

            user.save()
            return HttpResponseRedirect('../')
    else:
        form = CustomUserChangeForm(instance=user, caller_is_admin=request.user.is_admin)

    return render(request, 'login/edit_user.html', {'form': form, 'permissions': user.user_permissions.all()})


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


@permission_required('login.add_customuser')
def add_user(request):
    """
    View function for adding a book.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, caller_is_admin=request.user.is_admin)
        if form.is_valid():
            user = form.save(commit=True)
            user.creator_email = request.user.email
            user.save()
            form.save(commit=True)
            return HttpResponseRedirect('../')
    else:
        form = CustomUserCreationForm(caller_is_admin=request.user.is_admin)

    return render(request, 'add_user.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
