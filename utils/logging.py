from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.contrib.admin.models import LogEntry, ADDITION, DELETION, CHANGE
from library.models.documents import Book, Article, Video, Audio
from library.models.request_queue import RequestQueueElement
from library.models.record import Record
from library.models.author import Author
from library.models.tag import Tag
from login.models import CustomUser


def log_email(object):
    LogEntry.objects.log_action(
        user_id=object.created_by.id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=ADDITION,
        change_message=_('email sent')
    )


def log_addition(object):
    keys = [str(x) for x in object.__dict__.keys() if not x.startswith('_')]
    values = [str(x) for x in object.__dict__.values()][1:]

    type = dict(zip(keys, values))

    LogEntry.objects.log_action(
        user_id=1,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=ADDITION,
        change_message=_(str(type))
    )


def log_change(object):
    keys = [str(x) for x in object.__dict__.keys() if not x.startswith('_')]
    values = [str(x) for x in object.__dict__.values()][1:]

    type = dict(zip(keys, values))

    LogEntry.objects.log_action(
        user_id=1,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=CHANGE,
        change_message=_(str(type))
    )


def log_delete(object):
    keys = [str(x) for x in object.__dict__.keys() if not x.startswith('_')]
    values = [str(x) for x in object.__dict__.values()][1:]

    type = dict(zip(keys, values))

    LogEntry.objects.log_action(
        user_id=1,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=DELETION,
        change_message=_(str(type))
    )


def get_type(object):
    if isinstance(object, Book):
        return 'Book'
    elif isinstance(object, Article):
        return 'Article'
    elif isinstance(object, Video):
        return 'Video'
    elif isinstance(object, Audio):
        return 'Audio'
    elif isinstance(object, CustomUser):
        return 'User'
    elif isinstance(object, RequestQueueElement):
        return 'Request Queue'
    elif isinstance(object, Author):
        return 'Author'
    elif isinstance(object, Tag):
        return 'Tag'
    elif isinstance(object, Record):
        return 'Record'
    else:
        if object.outstanding:
            return 'Outstanding request made'
        else:
            return 'Outstanding request cancelled'
