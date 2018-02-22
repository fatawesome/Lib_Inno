from django.forms import ModelForm

from .models import *


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'tags', 'reference', 'publisher', 'edition', 'is_bestseller', 'price']
