from django.shortcuts import render

from library.models import *


def index(request):
    """
    View function for home page of site.
    """
    num_docs = Document.objects.all().count()
    num_instances = Record.objects.all().count() # number of copies of this document
    num_instances_available = Record.objects.filter(
        status='a').count() # number of available copies of this document
    num_authors = Author.objects.count() # number of authors

    return render(
        request,
        'index.html',
        context={'num_docs': num_docs, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors},
    )
