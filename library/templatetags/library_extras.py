from django import template
from library.models.documents import Book
import datetime

register = template.Library()

@register.filter
def is_owned_by_user(document, user):
    return document.record_set.filter(user=user).count() == 1 and document.record_set.get(user=user).status == 'o'

@register.filter
def is_reserved_by_user(document, user):
    return document.record_set.filter(user=user).count() == 1 and document.record_set.get(user=user).status == 'r'

@register.filter
def taken_by(document):
    users = list()
    for rec in document.record_set.filter(status='o'):
        users.append((rec.user.email, rec.user.first_name, rec.user.last_name, rec.due_to, rec.user))
    return users

@register.filter
def reserved_by(document):
    users = list()
    for rec in document.record_set.filter(status='r'):
        users.append((rec.user.email, rec.user.first_name, rec.user.last_name, rec.user))
    return users

@register.filter
def due_to(document, user):
    record = document.record_set.get(user=user)
    return record.due_to

@register.filter
def is_reference_book(document):
    if Book.objects.all().filter(id=document.id).count() != 0:
        return Book.objects.get(id=document.id).reference
    return False

@register.filter
def get_year(document):
    if Book.objects.all().filter(id=document.id).count() != 0:
        book = Book.objects.all().get(id=document.id)
        return book.year
    return False

@register.filter
def available_copies_exist(document):
    return document.record_set.filter(status='a').count() != 0

@register.filter
def number_of_available_copies(document):
    return document.record_set.filter(status='a').count()

@register.filter
def number_of_checked_out_copies(document):
    return document.record_set.filter(status='o').count()

@register.filter
def number_of_reserved_copies(document):
    return document.record_set.filter(status='r').count()

@register.filter
def already_in_queue(document, user):
    return document.requestqueueelement_set.filter(user=user).count() != 0

@register.filter
def queue(document):
    return document.requestqueueelement_set.all()
