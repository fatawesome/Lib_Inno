from django.db import models
from library.models import *
from login.models import CustomUser


class RequestQueueElement(models.Model):
    """
    Every object of this class is an element of the queue for the particular document.
    Object contains date, priority, link on user and document.
    """
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    priority = models.IntegerField(default=0)

    creator_email = models.CharField(max_length=50, null=True, blank=True, default="root@root.com")

    def default_priority(self):
        """
        Method calculates default priority depending on user type.
        :return:
        """
        if self.user.subtype == 'Students':
            return 4
        elif self.user.subtype == 'Instructors':
            return 3
        elif self.user.subtype == 'TAs':
            return 2
        elif self.user.subtype == 'Visiting Professors':
            return 1
        elif self.user.subtype == 'Professors':
            return 0

    class Meta:
        ordering = ['-priority', 'date']

    def __str__(self):
        return self.user.get_full_name()
