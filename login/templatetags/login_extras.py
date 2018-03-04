from django import template
import datetime

register = template.Library()

@register.filter
def overdue_list(customuser_list):
    res = []
    for user in customuser_list:
        for rec in user.record_set.all():
            if rec.due_to < datetime.date.today():
                res.append(user)
                break
    return res

@register.filter
def is_debtor(user):
    for rec in user.record_set.all():
        if rec.due_to < datetime.date.today():
            return True
    return False

@register.filter
def overdue_books_list(customuser_list, user):
    res = []
    for rec in user.record_set.all():
        if rec.due_to < datetime.date.today():
            res.append(rec.document)
    return res