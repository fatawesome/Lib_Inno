from django.db import models
from library.models import *
from login.models import CustomUser


class RequestQueue(models.Model):
    date = models.DateField()
    users = models.ManyToManyField(CustomUser, help_text='Add users for this queue')

    GROUP_PRIORITY = (
        (1, 'Faculty'),
        (2, 'Student'),
    )
    group_priority = models.IntegerField(choices=GROUP_PRIORITY)

    class Meta:
        ordering = ['group_priority', 'date']
