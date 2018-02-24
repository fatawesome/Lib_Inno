from django import template
import datetime

register = template.Library()


@register.filter
def is_owned_by_user(document, user):
    return document.record_set.filter(user=user).count() == 1


@register.filter
def due_to(document, user):
    record = document.record_set.get(user=user)
    return record.due_to
