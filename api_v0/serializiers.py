from rest_framework import serializers
from library.models import *


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'title',
            'authors',
            'price',
            'url',
        ]


class BookPreviewSerializer(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        model = Book
        fields = DocumentSerializer.Meta.fields + ['is_bestseller', ]


class BookDetailSerializer(BookPreviewSerializer):
    class Meta(BookPreviewSerializer.Meta):
        model = Book
        fields = BookPreviewSerializer.Meta.fields + ['publisher', 'edition']
        fields.remove('url')


class ArticlePreviewSerializer(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        model = Article
        fields = DocumentSerializer.Meta.fields + ['journal']


class ArticleDetailSerializer(ArticlePreviewSerializer):
    class Meta(ArticlePreviewSerializer.Meta):
        fields = ArticlePreviewSerializer.Meta.fields + ['editor']
        fields.remove('url')
