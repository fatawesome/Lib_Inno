from django.db import models
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """
        :return: the url to access a particular Author.
        """
        return reverse('author-detail', args=str(self.id))

    def __str__(self):
        return '{1} {0}'.format(self.first_name, self.last_name)


class AuthorManager(models.Manager):
    def create_author(self, first_name, last_name, date_of_birth, date_of_death):
        author = self.create(first_name=first_name, last_name=last_name,
                           date_of_birth=date_of_birth, date_of_death=date_of_death)
        author.save()
        return author
