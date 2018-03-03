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


class DocumentChangeForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title',
                  'authors',
                  'price',
                  'tags'
        )



class BookChangeForm(DocumentChangeForm):
    """
    A form for updating books
    """
    class Meta:
        model = Book
        fields = DocumentChangeForm.Meta.fields + ('reference',
                  'publisher',
                  'edition',
                  'is_bestseller'
                )


class ArticleForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Article
        fields = ['title', 'authors', 'tags', 'reference', 'editor', 'journal', 'price']


class ArticleChangeForm(DocumentChangeForm):
    class Meta:
        model = Article
        fields = DocumentChangeForm.Meta.fields + (
            'editor',
            'journal',
        )


class AudioForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Audio
        fields = ['title', 'authors', 'tags', 'price']


class AudioChangeForm(DocumentChangeForm):
    class Meta:
        model = Audio
        fields = DocumentChangeForm.Meta.fields


class VideoForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Video
        fields = ['title', 'authors', 'tags', 'price']


class VideoChangeForm(DocumentChangeForm):
    class Meta:
        model = Video
        fields = DocumentChangeForm.Meta.fields
