from django import template
import datetime

register = template.Library()


@register.filter
def is_owned_by_user(document, user):
    return document.record_set.filter(user=user).count() == 1

@register.filter
def is_owned_by_someone(document):
    return document.record_set.filter(status='o').count() != 0

@register.filter
def is_reserved_by_someone(document):
    return document.record_set.filter(status='r').count() != 0

@register.filter
def owned_by(document):
    users = list()
    for rec in document.record_set.filter(status='o'):
        users.append((rec.user.email, rec.user.first_name, rec.user.last_name))
    return users

@register.filter
def reserved_by(document):
    users = list()
    for rec in document.record_set.filter(status='r'):
        users.append((rec.user.email, rec.user.first_name, rec.user.last_name))
    return users


@register.filter
def due_to(document, user):
    record = document.record_set.get(user=user)
    return record.due_to