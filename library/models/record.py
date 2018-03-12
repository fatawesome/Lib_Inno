from django.db import models
from .documents import Document
from login.models import CustomUser

import uuid
import datetime

PENALTY = 100


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this book for the whole lib')
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    due_to = models.DateField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

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

    def get_overdue(self, date=datetime.date.today()):
        return (date - self.due_to).days

    def get_overdue_fine(self):
        days = self.get_overdue()
        if days > 0:
            return days * PENALTY
        else:
            return 0
