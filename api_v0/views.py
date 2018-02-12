from django.shortcuts import render

from rest_framework import viewsets
from .serializiers import *


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookPreviewSerializer
        return DocumentDetailSerializer
