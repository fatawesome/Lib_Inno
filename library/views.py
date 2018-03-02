from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import permission_required

from library.models import *
from .forms import BookForm
from .forms import ArticleForm
from .forms import *
from login.forms import *


def index(request):
    """
    View function for home page of site.
    """
    num_docs = Document.objects.all().count()
    num_instances = Record.objects.all().count()  # number of copies of this document
    num_instances_available = Record.objects.filter(
        status='a').count()  # number of available copies of this document
    num_authors = Author.objects.count()  # number of authors

    return render(
        request,
        'index.html',
        context={'num_docs': num_docs, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors},
    )


class DocumentListView(generic.ListView):
    """
    Generic class-based view listing all documents in the system.
    """
    model = Document
    paginate_by = 20

class AuthorListView(generic.ListView):
    """
    Generic class-based view listing all authors in the system.
    """
    model = Author
    paginate_by = 20

class DocumentDetailView(generic.DetailView):
    """
    Generic class-based view the particular document page.
    """
    model = Document


@permission_required('library.can_create')
def add_book(request):
    """
    View function for adding a book.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            document = form.save(commit=True)
            for _ in range(form.cleaned_data['num_of_copies']):
                Record.objects.create(document=document)
            return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect('document_detail/1')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})


def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            document = form.save(commit=True)
            for _ in range(form.cleaned_data['num_of_copies']):
                Record.objects.create(document=document)
            return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect('document_detail/1')
    else:
        form = ArticleForm()

    return render(request, 'add_article.html', {'form': form})


def add_audio(request):
    if request.method == 'POST':
        form = AudioForm(request.POST)
        if form.is_valid():
            document = form.save(commit=True)
            for _ in range(form.cleaned_data['num_of_copies']):
                Record.objects.create(document=document)
            return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect('document_detail/1')
    else:
        form = AudioForm()

    return render(request, 'add_audio.html', {'form': form})


def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            document = form.save(commit=True)
            for _ in range(form.cleaned_data['num_of_copies']):
                Record.objects.create(document=document)
            return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect('document_detail/1')
    else:
        form = VideoForm()

    return render(request, 'add_video.html', {'form': form})


# TODO: complete this view.
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm


def take_document(request, pk, doc_id):
    user = CustomUser.objects.get(id=pk)
    doc = Document.objects.get(id=doc_id)
    doc.take_from_user(user)
    return HttpResponseRedirect(user.get_absolute_url())


# TODO: rewrite using class-based view.
def claim(request, pk):
    if Book.objects.all().filter(id=pk).count() != 0:
        print('------------------')
        print()
        print('Book')
        print()
        print('------------------')
        doc = Book.objects.get(id=pk)
    elif Article.objects.all().filter(id=pk).count() != 0:
        print('------------------')
        print()
        print('Article')
        print()
        print('------------------')
        doc = Article.objects.get(id=pk)
    elif Audio.objects.all().filter(id=pk).count() != 0:
        print('------------------')
        print()
        print('Audio')
        print()
        print('------------------')
        doc = Audio.objects.get(id=pk)
    elif Video.objects.all().filter(id=pk).count() != 0:
        print('------------------')
        print()
        print('Video')
        print()
        print('------------------')
        doc = Video.objects.get(id=pk)
    else:
        print('------------------')
        print()
        print('ERROR')
        print()
        print('------------------')
        doc = None
    doc.give_to_user(request.user)
    return HttpResponseRedirect(reverse('documents'))


def delete_document(request, pk):
    doc = Document.objects.get(id=pk)
    doc.delete_document()
    return HttpResponseRedirect(reverse('documents'))


def edit_document(request, pk):
    """
    View function for editing a document.
    :param request:
    """
    doc = Document.objects.get(id=pk)
    print('------------------------')
    print(doc)
    print(type(doc))
    print(hasattr(doc, 'edition'))
    print(isinstance(doc, Book))
    print('------------------------')
    if request.method == 'POST':
        if hasattr(doc, 'edition'):
            form = BookChangeForm(request.POST)
        if form.is_valid():
            doc.title = form.cleaned_data['title']
            doc.authors = form.cleaned_data['authors']
            doc.tags = form.cleaned_data['tags']
            doc.reference = form.cleaned_data['reference']
            doc.price = form.cleaned_data['price']

            if isinstance(doc, Book):
                doc.publisher = form.cleaned_data['publisher']
                doc.edition = form.cleaned_data['edition']
                doc.is_bestseller = form.cleaned_data['is_bestseller']

            doc.save()
            return HttpResponseRedirect('../')
    else:
        if isinstance(doc, Book):
            form = BookChangeForm(instance=doc)
        else:
            form = BookChangeForm(instance=doc) # TODO delete this line

    return render(request, 'library/edit_document.html', {'form': form})