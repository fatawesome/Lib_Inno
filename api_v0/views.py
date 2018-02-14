from django.shortcuts import render

from rest_framework import viewsets
from .serializiers import *


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookPreviewSerializer
        return BookDetailSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticlePreviewSerializer
        return ArticleDetailSerializer
