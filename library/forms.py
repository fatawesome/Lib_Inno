from django.forms import ModelForm
<<<<<<< HEAD
from django import forms

=======
from login.models import *
>>>>>>> e3ac62ff2094a1e7a3417d0a5c162adac06138db
from .models import *
from login.models import CustomUser


class BookForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Book
<<<<<<< HEAD
        fields = ['title', 'authors', 'tags', 'reference',
                  'publisher', 'edition', 'is_bestseller', 'price']


class UserForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'password' 'first_name', 'last_name', 'phone_number', 'address']
=======
        fields = ['title', 'authors', 'tags', 'reference', 'publisher', 'edition', 'is_bestseller', 'price']


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
>>>>>>> e3ac62ff2094a1e7a3417d0a5c162adac06138db
