from django.db import models
from django.urls import reverse

from .author import Author
from .tag import Tag


class Document(models.Model):
    """
    Model representing any document in the system.
    """
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    authors = models.ManyToManyField(Author, help_text='Add authors for this document')
    tags = models.ManyToManyField(Tag, help_text='Add tags for this document')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        :return: the url to access a particular Document instance.
        """
        return reverse('document-detail', args=[str(self.id)])

    def display_authors(self):
        """
        Creates a string for the list of authors.
        :return: string of authors.
        """
        return ''.join([str(author) for author in self.authors.all()])

    def display_tags(self):
        """
        Creates a string for the list of tags
        :return: string of tags
        """
        return ''.join([tag.name for tag in self.tags.all()])

    def display_price(self):
        return self.price


class Book(Document):
    """
    Model represents general book.
    """
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField(default=1)
    is_bestseller = models.BooleanField(default=False)


class Article(Document):
    editor = models.CharField(max_length=100)
    journal = models.CharField(max_length=100)


class Audio(Document):
    content = models.CharField(max_length=200)


class Video(Document):
    content = models.CharField(max_length=200)






