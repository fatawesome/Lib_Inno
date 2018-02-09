from django.db import models
from django.urls import reverse

from .author import Author
from .tag import Tag

import datetime


class Document(models.Model):
    """
    Model representing any document in the system.
    """
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    authors = models.ManyToManyField(Author, help_text='Add authors for this document')
    tags = models.ManyToManyField(Tag, help_text='Add tags for this document')
    reference = models.BooleanField(default=False)

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

    def give_to_user(self, user):
        rec_set = self.record_set.filter(status='a')
        if rec_set.count() != 0 and self.id not in [x.document.id for x in user.record_set.all()] and not self.reference:
            record = rec_set.first()
            record.user = user
            record.status = 'o'
            record.due_to = datetime.date.today() + record.get_due_delta()
            record.save()


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






