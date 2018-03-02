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


class BookChangeForm(forms.ModelForm):
    """
    A form for updating books
    """

    class Meta:
        model = Book
        fields = ('title',
                  'authors',
                  'price',
                  'tags',
                  'reference',
                  'publisher',
                  'edition',
                  'is_bestseller',
                  )


class ArticleForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Article
        fields = ['title', 'authors', 'tags', 'reference', 'editor', 'journal', 'price']


class AudioForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Audio
        fields = ['title', 'authors', 'tags', 'price']


class VideoForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Audio
        fields = ['title', 'authors', 'tags', 'price']
