from django import template

register = template.Library()


@register.filter
def is_owned_by_user(document, user):
    return document.record_set.filter(user=user).count() == 1
