from django.db import models
from library.models import *
from login.models import CustomUser


class RequestQueue(models.Model):
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    GROUP_PRIORITY = (
        (1, 'Faculty'),
        (2, 'Student'),
    )
    group_priority = models.IntegerField(choices=GROUP_PRIORITY)

    class Meta:
        ordering = ['group_priority', 'date']
