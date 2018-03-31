from django.db import models
from library.models import *
from login.models import CustomUser


class RequestQueueElement(models.Model):
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    priority = models.IntegerField(default=0)

    def default_priority(self):
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

    # GROUP_PRIORITY = (
    #     (1, 'Faculty'),
    #     (2, 'Student'),
    # )
    # group_priority = models.IntegerField(choices=GROUP_PRIORITY)

    class Meta:
        ordering = ['-priority', 'date']
