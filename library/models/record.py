from django.db import models
from django.contrib.auth.models import User
from .documents import Document

import uuid
import datetime


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this book for the whole lib')
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    due_to = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Document availability')

    class Meta:
        ordering = ["due_back"]
        # TODO: define permissions
        permissions = ()

    # TODO: rewrite group conditions
    def get_due_delta(self):
        delta = 0
        if getattr(self.document, 'book') is not None:
            if self.borrower.groups.first().name == 'Faculty':
                delta = 4
            elif self.document.book.is_bestseller:
                delta = 2
            else:
                delta = 3
        else:
            if self.borrower.groups.first().name == 'Students':  # For students
                delta = 2
            else:
                delta = 3

        return datetime.timedelta(weeks=delta)

    def get_overdue_fine(self):
        days = (datetime.date.today() - self.due_to).days
        if days > 0:
            return days * 100
        else:
            return 0

    def give_to_user(self, user):
        self.user = user
        status = 'o'
        due_to = datetime.date.today() + self.get_due_delta()
