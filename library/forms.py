from django.forms import ModelForm
from login.models import *
from .models import *


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'tags', 'reference', 'publisher', 'edition', 'is_bestseller', 'price']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'authors', 'tags', 'reference', 'editor', 'journal', 'price']
