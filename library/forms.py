from django.forms import ModelForm
from django import forms

from login.models import *
from .models import *
from login.models import CustomUser


class SearchFrom(forms.Form):
    title = forms.CharField(max_length=200, required=False)
    authors = forms.CharField(max_length=200, required=False)
    tags = forms.CharField(max_length=200, required=False)
    available = forms.BooleanField(initial=False, required=False)
    taken = forms.BooleanField(initial=False, required=False)


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AddCopies(forms.Form):
    number_of_copies = forms.IntegerField()


class RemoveCopies(forms.Form):
    number_of_copies = forms.IntegerField()


class DocumentChangeForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title',
                  'authors',
                  'price',
                  'tags'
                  )


class BookForm(ModelForm):
    num_of_copies = forms.IntegerField()

    class Meta:
        model = Book
        fields = ['title', 'authors', 'tags', 'reference',
                  'publisher', 'edition', 'is_bestseller', 'price', 'year']


class BookChangeForm(DocumentChangeForm):
    """
    A form for updating books
    """

    class Meta:
        model = Book
        fields = DocumentChangeForm.Meta.fields + ('reference',
                                                   'publisher',
                                                   'edition',
                                                   'is_bestseller',
                                                   'year',
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
