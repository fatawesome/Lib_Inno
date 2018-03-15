from django.db import models
from library.models import *
from login.models import CustomUser


class RequestQueueElement(models.Model):
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
#    priority = models.IntegerField(default=(0 if 'Students' in [x.name for x in user.groups.all()] else 1))
    priority = models.IntegerField(default=0)

    def set_priority(self):
        if 'Students' in [x.name for x in self.user.groups.all()]:
            self.priority = 0
        elif 'Faculty' in [x.name for x in self.user.groups.all()]:
            self.priority = 1

    # GROUP_PRIORITY = (
    #     (1, 'Faculty'),
    #     (2, 'Student'),
    # )
    # group_priority = models.IntegerField(choices=GROUP_PRIORITY)

    class Meta:
        ordering = ['-priority', 'date']
