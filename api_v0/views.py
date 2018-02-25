from rest_framework import viewsets
from .serializiers import *


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Can be used to get list of Book objects in JSON
    """
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookPreviewSerializer
        return BookDetailSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Can be used to get list of Article objects in JSON
    """
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticlePreviewSerializer
        return ArticleDetailSerializer
