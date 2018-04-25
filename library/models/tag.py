from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)
    creator_email = models.CharField(max_length=50, null=True, blank=True, default="root@root.com")

    def __str__(self):
        return self.name
