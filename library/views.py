from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail, BadHeaderError
from .models.request_queue import RequestQueueElement
from library import views
import datetime

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
    """
    View for listing document of user with given id.
    :param request: HTTP request.
    :param pk: user id.
    :return: rendered page with list of user's documents.
    """
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
    """
    Add article view.
    :param request: HTTP request.
    :return: HTTP redirect.
    """
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

    return render(request, 'add_article.html',
                  {'article_form': article_form, 'author_form': author_form, 'tag_form': tag_form})


@permission_required('library.can_create')
def add_audio(request):
    """
    Add audio view.
    :param request: HTTP request.
    :return: HTTP redirect.
    """
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

    return render(request, 'add_audio.html',
                  {'audio_form': audio_form, 'author_form': author_form, 'tag_form': tag_form})


@permission_required('library.can_create')
def add_video(request):
    """
    Add video view.
    :param request: HTTP request.
    :return: HTTP redirect
    """
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

    return render(request, 'add_video.html',
                  {'video_form': video_form, 'author_form': author_form, 'tag_form': tag_form})


@permission_required('library.can_create')
def add_copies(request, pk):
    """
    Adds copies of document with given id.
    :param request: HTTP request.
    :param pk: document id.
    :return: HTTP redirect to document page.
    """
    doc = Document.objects.get(id=pk)
    if request.method == 'POST':
        form = AddCopies(request.POST)
        if form.is_valid():
            number_of_copies = form.cleaned_data['number_of_copies']

            for _ in range(number_of_copies):
                Record.objects.create(document=doc)

            update_request_queue(doc)

        return HttpResponseRedirect(reverse('document-detail', args=[pk]))


@permission_required('library.can_delete')
def remove_copies(request, pk):
    """
    Removes copies of document with given id.
    :param request: HTTP request.
    :param pk: document id.
    :return: HTTP redirect to document page.
    """
    doc = Document.objects.get(id=pk)
    if request.method == 'POST':
        form = RemoveCopies(request.POST)
        if form.is_valid():
            number_of_copies = form.cleaned_data['number_of_copies']
            to_delete = min(number_of_copies, Record.objects.filter(status='a', document=doc).count())
            for _ in range(to_delete):
                rec = Record.objects.filter(status='a', document=doc).first()
                rec.delete()
        return HttpResponseRedirect(reverse('document-detail', args=[pk]))


@permission_required('library.can_change')
def take_document(request, pk, user_id):
    """
    Return a document to the system.
    :param request: HTTP request.
    :param pk: document id.
    :param user_id: user id.
    :return: HTTP redirect to user page.
    """
    user = CustomUser.objects.get(id=user_id)
    doc = Document.objects.get(id=pk)
    doc.take_from_user(user)

    update_request_queue(doc)  # give this record to first user in the queue

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@permission_required('library.can_change')
def delete_copy(request, pk, user_id):
    """
    Delete a copy of the document
    :param request: HTTP request.
    :param pk: id of document.
    :param user_id: id of user.
    :return: HTTP redirect to user page.
    """
    user = CustomUser.objects.get(id=user_id)
    doc = Document.objects.get(id=pk)
    rec = user.record_set.get(document=doc)
    rec.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_object_of_class(pk):
    """
    Recognize type of model inherited from Document by primary key.
    :param pk: id.
    :return: instance of model, inherited from Document.
    """
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
    """
    Set document reserved by user.
    :param request: HTTP request.
    :param doc_id: id of document
    :return:
    """
    doc = get_object_of_class(doc_id)
    doc.reserve_by_user(request.user)
    return HttpResponseRedirect(reverse('document-detail', args=[doc_id]))


def renew_document(request, doc_id):
    """
    Feature to renew (take again) document by user
    :param doc_id: document to renew by request.user
    """
    rec = get_object_of_class(doc_id).record_set.get(user=request.user)
    rec.renew_by_user(request.user)
    return HttpResponseRedirect(reverse('document-detail', args=[doc_id]))


def update_request_queue(document):
    """
    Give available copies to someone in the request queue.
    :param document: Object of model Document.
    """
    while Record.objects.filter(status='a', document=document).count() != 0:
        if document.requestqueueelement_set.count() == 0:
            break
        user = document.requestqueueelement_set.first().user

        send_mail(
            'Document is available',
            'Document "' + document.title + '" is reserved by You.\n You have 1 day to take it from the library.',
            'fatawesomeee@yandex.ru',
            [user.email],
            fail_silently=False
        )

        document.reserve_by_user(user)


def get_in_queue(request, doc_id):
    """
    Get user into queue.
    :param request: HTTP request.
    :param doc_id: document id.
    :return: HTTP redirect to document detail page.
    """
    doc = get_object_of_class(doc_id)
    if not doc.outstanding:
        element = RequestQueueElement.objects.create(document=doc, user=request.user, date=datetime.date.today())
        element.priority = element.default_priority()
        element.save()
    return HttpResponseRedirect(reverse('document-detail', args=[doc_id]))


def quit_queue(request, doc_id):
    """
    Remove user from queue.
    :param request: HTTP request.
    :param doc_id: document id.
    :return: HTTP redirect to document detail page.
    """
    doc = get_object_of_class(doc_id)
    element = RequestQueueElement.objects.get(document=doc, user=request.user)
    element.delete()
    return HttpResponseRedirect(reverse('document-detail', args=[doc_id]))


@permission_required('library.can_change')
def give_document(request, doc_id, user_id):
    """
    Give document to user.
    :param request: HTTP request.
    :param doc_id: document id.
    :param user_id: user id.
    :return: HTTP redirect to user detail page.
    """
    doc = get_object_of_class(doc_id)
    user = CustomUser.objects.get(id=user_id)
    rec = user.record_set.get(document=doc)
    doc.give_to_user(user, rec)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@permission_required('library.can_change')
def increase_user_priority(request, doc_id, user_id):
    """
    Increases user priority in queue.
    :param request: HTTP request.
    :param doc_id: document id.
    :param user_id: user id.
    :return: HTTP redirect to document detail page.
    """
    doc = get_object_of_class(doc_id)
    user = CustomUser.objects.get(id=user_id)
    element = RequestQueueElement.objects.get(document=doc, user=user)
    element.priority = max([x.priority for x in RequestQueueElement.objects.filter(document=doc).all()]) + 1
    element.save()
    return HttpResponseRedirect(reverse('document-detail', args=[doc_id]))


@permission_required('library.can_change')
def reset_user_priority(request, doc_id, user_id):
    """
    Resets user priority in queue to default.
    :param request: HTTP request.
    :param doc_id: document id.
    :param user_id: user id.
    :return: HTTP redirect to document detail page.
    """
    doc = get_object_of_class(doc_id)
    user = CustomUser.objects.get(id=user_id)
    element = RequestQueueElement.objects.get(document=doc, user=user)
    element.priority = element.default_priority()
    element.save()
    return HttpResponseRedirect(reverse('document-detail', args=[doc_id]))


@permission_required('library.can_delete')
def delete_document(request, pk):
    """
    Deletes document with the given id.
    :param request: HTTP request.
    :param pk: document id.
    :return: HTTP redirect to document list page
    """
    doc = get_object_of_class(pk)
    for queue_elem in doc.requestqueueelement_set.all():
        queue_elem.delete()
    doc.delete_document()
    return HttpResponseRedirect(reverse('documents'))


@permission_required('library.can_change')
def edit_document(request, pk):
    """
    View function for editing a document.
    :param pk: document id.
    :param request:
    :return: rendered edit_document page.
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
                doc.year = form.cleaned_data['year']
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


@permission_required('library.can_change')
def document_outstanding_request(request, doc_id):
    """
    Activate outstanding request for document with given id.
    :param request: HTTP request.
    :param doc_id: document id.
    :return: HTTP redirect to document detail page.
    """
    doc = Document.objects.get(id=doc_id)
    doc.outstanding_request()
    return HttpResponseRedirect(reverse('document-detail', args=[doc_id]))


@permission_required('library.can_change')
def document_disable_outstanding_request(request, doc_id):
    """
    Deactivates outstanding request for document with given id.
    :param request: HTTP request.
    :param doc_id: document id.
    :return: HTTP redirect to document detail page.
    """
    doc = get_object_of_class(doc_id)
    doc.disable_outstanding_request()
    return HttpResponseRedirect(reverse('document-detail', args=[doc_id]))


@permission_required('library.can_delete')
def ask_for_return(request, pk, user_id):
    """
    Send a notification to user that he needs to return a book.
    :param request: HTTP request.
    :param pk: document id.
    :param user_id: user id.
    :return: HTTP redirect on user page.
    """
    user = CustomUser.objects.get(id=user_id)
    doc = Document.objects.get(id=pk)
    send_mail(
        'Return document',
        'Please, return ' + doc.title + ' back to the library.',
        'fatawesomeee@yandex.ru',
        [user.email],
        fail_silently=False
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
