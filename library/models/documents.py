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
        """
        Gives a document to user
        """
        rec_set = self.record_set.filter(status='a')
        if rec_set.count() != 0 and self.id not in [x.document.id for x in user.record_set.all()] and not self.reference:
            record = rec_set.first()
            record.user = user
            record.status = 'o'
            record.due_to = datetime.date.today() + self.get_due_delta(user)
            record.save()

    def take_from_user(self, user):
        """
        Takes a document from user.
        :param user:
        :return:
        """
        record = user.record_set.filter(document=self).first()
        record.due_to = None
        record.user = None
        record.status = 'a'
        record.save()
        user.save()

    def get_due_delta(self, user):
        delta = 0
        if isinstance(self, Book):
            if 'Faculty' in [x.name for x in user.groups.all()]:
                delta = 4
            elif self.is_bestseller:
                delta = 2
            else:
                delta = 3
        else:
            if 'Students' in [x.name for x in user.groups.all()]:
                delta = 2
            else:
                delta = 3

        return datetime.timedelta(weeks=delta)


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






