from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail, BadHeaderError
from library import views

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
        author_form = AuthorForm(request.POST)
        book_form = BookForm(request.POST)
        tag_form = TagForm(request.POST)

        if tag_form.is_valid():
            tag_form.save(commit=True)
            return HttpResponseRedirect(reverse('add_book'))

        if author_form.is_valid():
            author_form.save(commit=True)
            return HttpResponseRedirect(reverse('add_book'))

        if book_form.is_valid():
            document = book_form.save(commit=True)
            for _ in range(book_form.cleaned_data['num_of_copies']):
                Record.objects.create(document=document)
            return HttpResponseRedirect('../')
    else:
        author_form = AuthorForm()
        book_form = BookForm()
        tag_form = TagForm()

    return render(request, 'add_book.html', {'book_form': book_form, 'author_form': author_form, 'tag_form': tag_form})


@permission_required('library.can_create')
def add_article(request):
    if request.method == 'POST':
        author_form = AuthorForm(request.POST)
        article_form = ArticleForm(request.POST)
        tag_form = TagForm(request.POST)

        if tag_form.is_valid():
            tag_form.save(commit=True)
            return HttpResponseRedirect(reverse('add_article'))

        if author_form.is_valid():
            author_form.save(commit=True)
            return HttpResponseRedirect(reverse('add_article'))

        if article_form.is_valid():
            document = article_form.save(commit=True)
            for _ in range(article_form.cleaned_data['num_of_copies']):
                Record.objects.create(document=document)
            return HttpResponseRedirect('../')
    else:
        author_form = AuthorForm()
        article_form = ArticleForm()
        tag_form = TagForm()

    return render(request, 'add_article.html', {'article_form': article_form, 'author_form': author_form, 'tag_form': tag_form})


@permission_required('library.can_create')
def add_audio(request):
    if request.method == 'POST':
        author_form = AuthorForm(request.POST)
        audio_form = AudioForm(request.POST)
        tag_form = TagForm(request.POST)

        if tag_form.is_valid():
            tag_form.save(commit=True)
            return HttpResponseRedirect(reverse('add_audio'))

        if author_form.is_valid():
            author_form.save(commit=True)
            return HttpResponseRedirect(reverse('add_audio'))

        if audio_form.is_valid():
            document = audio_form.save(commit=True)
            for _ in range(audio_form.cleaned_data['num_of_copies']):
                Record.objects.create(document=document)
            return HttpResponseRedirect('../')
    else:
        author_form = AuthorForm()
        audio_form = AudioForm()
        tag_form = TagForm()

    return render(request, 'add_audio.html', {'audio_form': audio_form, 'author_form': author_form, 'tag_form': tag_form})


@permission_required('library.can_create')
def add_video(request):
    if request.method == 'POST':
        author_form = AuthorForm(request.POST)
        video_form = VideoForm(request.POST)
        tag_form = TagForm(request.POST)

        if tag_form.is_valid():
            tag_form.save(commit=True)
            return HttpResponseRedirect(reverse('add_video'))

        if author_form.is_valid():
            author_form.save(commit=True)
            return HttpResponseRedirect(reverse('add_video'))

        if video_form.is_valid():
            document = video_form.save(commit=True)
            for _ in range(video_form.cleaned_data['num_of_copies']):
                Record.objects.create(document=document)
            return HttpResponseRedirect('../')
    else:
        author_form = AuthorForm()
        video_form = VideoForm()
        tag_form = TagForm()

    return render(request, 'add_video.html', {'video_form': video_form, 'author_form': author_form, 'tag_form': tag_form})


@permission_required('library.can_create')
def add_copies(request, pk):
    doc = Document.objects.get(id=pk)
    if request.method == 'POST':
        form = AddCopies(request.POST)
        if form.is_valid():
            number_of_copies = form.cleaned_data['number_of_copies']
            for _ in range(number_of_copies):
                Record.objects.create(document=doc)
        return HttpResponseRedirect(reverse('document-detail', args=[pk]))


@permission_required('library.can_change')
def take_document(request, pk, user_id):
    """
    Return a document to the system.
    :return:
    """
    user = CustomUser.objects.get(id=user_id)
    doc = Document.objects.get(id=pk)
    doc.take_from_user(user)
    return HttpResponseRedirect(user.get_absolute_url())

@permission_required('library.can_change')
def delete_copy(request, pk, user_id):
    """
    Delete a copy of the document
    """
    user = CustomUser.objects.get(id=user_id)
    doc = Document.objects.get(id=pk)
    rec = user.record_set.get(document=doc)
    rec.delete()
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


def reserve(request, doc_id):
    doc = get_object_of_class(doc_id)

    doc.reserve_by_user(request.user)
    pk = doc_id
    return HttpResponseRedirect(reverse('document-detail', args=[pk]))


@permission_required('library.can_change')
def give_document(request, doc_id, user_id):
    doc = get_object_of_class(doc_id)
    user = CustomUser.objects.get(id=user_id)
    rec = user.record_set.get(document=doc)


    doc.give_to_user(request.user, rec)
    return HttpResponseRedirect(reverse('customuser_detail', args=[user_id]))


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
def ask_for_return(request, pk, user_id):
    user = CustomUser.objects.get(id=user_id)
    doc = Document.objects.get(id=pk)
    send_mail(
        'Return document',
        'Please, return ' + doc.title + ' back to the library.',
        'fatawesomeee@yandex.ru',
        [user.email],
        fail_silently=False
    )
    return HttpResponseRedirect(user.get_absolute_url())




