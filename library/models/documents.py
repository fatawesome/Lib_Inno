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

    class Meta:
        permissions = (('can_create', 'Create new document'),
                       ('can_delete', 'Delete document'),
                       ('can_change', 'Change document'))

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
        return self.authors.all()

    def display_tags(self):
        """
        Creates a string for the list of tags
        :return: string of tags
        """
        return ', '.join([tag.name for tag in self.tags.all()])

    def display_price(self):
        return self.price

    def give_to_user(self, user, record, date=datetime.date.today()):
        """
        Gives a document to user
        """
        if record.status == 'r':
            record.status = 'o'
            record.due_to = date + self.get_due_delta(user)
            record.save()

    def reserve_by_user(self, user):
        """
        Reserve a document by user
        """
        rec_set = self.record_set.filter(status='a')
        if rec_set.count() != 0 and self.id not in [x.document.id for x in user.record_set.all()] and not self.reference:# Why do we check it second time?

            if user.requestqueueelement_set.filter(document=self).count() != 0: # If the user in the request queue
                user.requestqueueelement_set.get(document=self).delete()        # remove it from there

            record = rec_set.first()
            record.user = user
            record.status = 'r'
            record.save()

    def delete_document(self):
        """
        Delete current document and all it's records
        """
        for rec in self.record_set.all():
            rec.delete()
        self.delete()

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
        """
        Counts for how many weeks document can be taken
        """
        if isinstance(self, Book):
            if 'Faculty' in [x.name for x in user.groups.all()]:
                delta = 4
            elif self.is_bestseller:
                delta = 2
            else:
                delta = 3
        else:
            delta = 2

        return datetime.timedelta(weeks=delta)

    def get_number_of_available_copies(self):
        """
        Gets number of available copies of current document
        :return:
        """
        return self.record_set.filter(status="a").count()

    def is_owned_by_user(self, user):
        """
        Evaluate if current document is owned by a user
        :param user:
        :return: true if document is already taken by user
        """
        return self.record_set.filter(user=user).count() == 1


# TODO: Add tags to creation method.
class BookManager(models.Manager):
    def create_book(self, title, price, reference, authors, publisher, is_bestseller, edition, year):
        book = self.create(title=title, price=price,
                           reference=reference, publisher=publisher,
                           is_bestseller=is_bestseller, edition=edition, year=year)
        book.authors.set(authors)
        book.save()
        return book


class Book(Document):
    """
    Model represents general book.
    """
    objects = BookManager()
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField(default=1)
    is_bestseller = models.BooleanField(default=False)
    year = models.IntegerField(default=2000)


class ArticleManager(models.Manager):
    def create_article(self, title, price, reference, authors, editor, journal):
        article = self.create(title=title, price=price,
                              reference=reference, editor=editor, journal=journal)
        article.authors.set(authors)
        article.save()
        return article


class Article(Document):
    editor = models.CharField(max_length=100)
    journal = models.CharField(max_length=100)


class AudioManager(models.Manager):
    def create_audio(self, title, authors, price, content):
        audio = self.create(title=title, price=price,
                            content=content)
        audio.authors.set(authors)
        audio.save()
        return audio


class Audio(Document):
    objects = AudioManager()
    content = models.CharField(max_length=200)


class VideoManager(models.Manager):
    def create_video(self, title, authors, price, content):
        video = self.create(title=title, price=price,
                            content=content)
        video.authors.set(authors)
        video.save()
        return video


class Video(Document):
    objects = VideoManager()
    content = models.CharField(max_length=200)
