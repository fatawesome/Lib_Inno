from django.forms import ModelForm
from django import forms

from login.models import *
from .models import *
from login.models import CustomUser


class BookForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Book
        fields = ['title', 'authors', 'tags', 'reference',
                  'publisher', 'edition', 'is_bestseller', 'price']

class BookDeleteForm(ModelForm):
    class Meta:
        model = Document
        fields = ['title']


class UserForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'address']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'authors', 'tags', 'reference', 'editor', 'journal', 'price']


class AudioForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'authors', 'tags', 'price']


class VideoForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'authors', 'tags', 'price']
