from .documents import *
from login.models import CustomUser

import uuid
import datetime

PENALTY = 100


def get_object_of_class(pk):
    """
    Recognize type of model inherited from Document by primary key.
    :param pk: id.
    :return: instance of model, inherited from Document.
    """
    doc = None

    if Book.objects.all().filter(id=pk).count() != 0:
        doc = Book.objects.get(id=pk)
    elif Article.objects.all().filter(id=pk).count() != 0:
        doc = Article.objects.get(id=pk)
    elif Audio.objects.all().filter(id=pk).count() != 0:
        doc = Audio.objects.get(id=pk)
    elif Video.objects.all().filter(id=pk).count() != 0:
        doc = Video.objects.get(id=pk)

    return doc


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this book for the whole lib')
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    due_to = models.DateField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    renewals_left = models.IntegerField(default=1)

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

    def make_available(self):
        self.due_to = None
        self.user = None
        self.status = 'a'
        self.renewals_left = 1
        self.save()

    def renew_by_user(self, user, date=None):
        """
        Recalculate due_to for user, update counter of renewals
        :param user: user, that wants to renew document
        """
        if date is None:
            date = datetime.date.today()
        if self.renewals_left > 0 and not self.document.outstanding:
            if user.subtype != 'Visiting Professors':
                self.renewals_left -= 1
            self.due_to = date + self.get_due_delta()
            self.save()

    def get_overdue(self, date=datetime.date.today()):
        return (date - self.due_to).days

    def get_overdue_fine(self):
        days = self.get_overdue()
        if days > 0:
            if days * PENALTY <= self.document.price:
                return days * PENALTY
            else:
                return self.document.price
        else:
            return 0

    def get_due_delta(self):
        """
        Counts for how many weeks document can be taken
        """
        real_type = get_object_of_class(self.document.id)
        if 'Visiting Professors' in [x.name for x in self.user.groups.all()]:
            delta = 1
        elif isinstance(real_type, Book):
            if 'Faculty' in [x.name for x in self.user.groups.all()]:
                delta = 4
            elif real_type.is_bestseller:
                delta = 2
            else:
                delta = 3
        else:
            delta = 2

        return datetime.timedelta(weeks=delta)