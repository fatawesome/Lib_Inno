from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    paginate_by = 5


class AuthorListView(generic.ListView):
    """
    Generic class-based v   iew listing all authors in the system.
    """
    model = Author
    paginate_by = 5


class DocumentDetailView(generic.DetailView):
    """
    Generic class-based view the particular document page.
    """
    model = Document


# TODO: rewrite using class-based view.
def add_book(request):
    """
    View function for adding a book.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        form.as_p
        if form.is_valid():
            # Book.objects.create_book(form.title, form.price, form.reference,
            #                          form.authors, form.publisher, form.is_bestseller, form.edition)
            form.save(commit=True)
            return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect('document_detail/1')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

def add_user(request):
    """
    View function for adding a book.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Book.objects.create_book(form.title, form.price, form.reference,
            #                          form.authors, form.publisher, form.is_bestseller, form.edition)
            form.save(commit=True)
            return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect('document_detail/1') # DOCUMENT_DETAIL
    else:
        form = CustomUserCreationForm()

    return render(request, 'add_user.html', {'form': form})


def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
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
            form.save(commit=True)
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
            form.save(commit=True)
            return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect('document_detail/1')
    else:
        form = VideoForm()

    return render(request, 'add_video.html', {'form': form})

# TODO: rewrite using class-based view.
def claim_document(request, pk):
    doc = Document.objects.get(id=pk)
    doc.give_to_user(request.user)
    return HttpResponseRedirect(reverse('documents'))
