from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail, BadHeaderError

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


def my_documents(request, pk):
    return render(request, 'library/my_documents_list.html', {'user': CustomUser.objects.get(id=pk)})


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


@permission_required('library.can_create')
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


@permission_required('library.can_create')
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


@permission_required('library.can_create')
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


@permission_required('library.can_create')
def add_copies(request, pk):
    doc = Document.objects.get(id=pk)
    if request.method == 'POST':
        form = AddCopies(request.POST)
        if form.is_valid():
            number_of_copies = form.cleaned_data['number_of_copies']
            for _ in range(number_of_copies):
                Record.objects.create(document=doc)
        else:
            render(request, 'library/document_detail.html', {'add_copies_form': form})
        return HttpResponseRedirect(reverse('documents'))
    else:
        form = AddCopies()

    return render(request, 'document_detail.html', {'add_copies_form': form})


@permission_required('library.can_change')
def take_document(request, pk, doc_id):
    """
    Return a document to the system.
    :return:
    """
    user = CustomUser.objects.get(id=pk)
    doc = Document.objects.get(id=doc_id)
    doc.take_from_user(user)
    return HttpResponseRedirect(user.get_absolute_url())


def get_object_of_class(pk):
    if Book.objects.all().filter(id=pk).count() != 0:
        doc = Book.objects.get(id=pk)
    elif Article.objects.all().filter(id=pk).count() != 0:
        doc = Article.objects.get(id=pk)
    elif Audio.objects.all().filter(id=pk).count() != 0:
        doc = Audio.objects.get(id=pk)
    elif Video.objects.all().filter(id=pk).count() != 0:
        doc = Video.objects.get(id=pk)

    return doc


def claim(request, pk):
    doc = get_object_of_class(pk)

    doc.give_to_user(request.user)
    return HttpResponseRedirect(reverse('documents'))


@permission_required('library.can_delete')
def delete_document(request, pk):
    doc = Document.objects.get(id=pk)
    doc.delete_document()
    return HttpResponseRedirect(reverse('documents'))


@permission_required('library.can_change')
def edit_document(request, pk):
    """
    View function for editing a document.
    :param request:
    """

    doc = get_object_of_class(pk)

    if request.method == 'POST':
        if isinstance(doc, Book):
            form = BookChangeForm(request.POST)
        elif isinstance(doc, Article):
            form = ArticleChangeForm(request.POST)
        elif isinstance(doc, Audio):
            form = AudioChangeForm(request.POST)
        elif isinstance(doc, Video):
            form = VideoChangeForm(request.POST)

        if form.is_valid():
            doc.title = form.cleaned_data['title']
            doc.authors.set(form.cleaned_data['authors'])
            doc.tags.set(form.cleaned_data['tags'])
            doc.price = form.cleaned_data['price']

            if isinstance(doc, Book):
                doc.publisher = form.cleaned_data['publisher']
                doc.edition = form.cleaned_data['edition']
                doc.is_bestseller = form.cleaned_data['is_bestseller']
            elif isinstance(doc, Article):
                doc.editor = form.cleaned_data['editor']
                doc.journal = form.cleaned_data['journal']

            doc.save()
            return HttpResponseRedirect('../')
    else:
        if isinstance(doc, Book):
            form = BookChangeForm(instance=doc)
        elif isinstance(doc, Article):
            form = ArticleChangeForm(instance=doc)
        elif isinstance(doc, Audio):
            form = AudioChangeForm(instance=doc)
        elif isinstance(doc, Video):
            form = VideoChangeForm(instance=doc)

    return render(request, 'library/edit_document.html', {'form': form})


@permission_required('library.can_delete')
def ask_for_return(request, pk, doc_id):
    user = CustomUser.objects.get(id=pk)
    doc = Document.objects.get(id=doc_id)
    send_mail(
        'Return document',
        'Please, return ' + doc.title + ' back to the library.',
        'fatawesomeee@yandex.ru',
        [user.email],
        fail_silently=False
    )
    return HttpResponseRedirect(user.get_absolute_url())




