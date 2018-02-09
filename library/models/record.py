from django.db import models
from django.contrib.auth.models import User, Group
from .documents import Document

import uuid
import datetime


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this book for the whole lib')
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    due_to = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # TODO: make enum
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='a', help_text='Document availability')

    class Meta:
        ordering = ["due_to"]
        # TODO: define permissions
        permissions = ()

    def get_overdue_fine(self):
        days = (datetime.date.today() - self.due_to).days
        if days > 0:
            # TODO: make magic num constant
            return days * 100
        else:
            return 0

    # TODO: move to Document model.
    def take_from_user(self):
        self.user = None
        self.status = 'a'
        self.due_to = None
        self.save()
