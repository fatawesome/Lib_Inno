from django.forms import ModelForm
from django import forms

from .models import *
from login.models import CustomUser


class BookForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Book
        fields = ['title', 'authors', 'tags', 'reference',
                  'publisher', 'edition', 'is_bestseller', 'price']


class UserForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'password' 'first_name', 'last_name', 'phone_number', 'address']
