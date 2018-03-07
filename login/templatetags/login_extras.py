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
        if rec.status=='o' and rec.due_to < datetime.date.today():
            return True
    return False

@register.filter
def overdue_document(user, doc):
    return user.record_set.get(document=doc).due_to < datetime.date.today()


@register.filter
def overdue_books_list(customuser_list, user):
    res = []
    for rec in user.record_set.all():
        if rec.due_to < datetime.date.today():
            res.append(rec.document)
    return res

@register.filter
def taken_books_list(customuser):
    return customuser.record_set.filter(status='o')

@register.filter
def reserved_books_list(customuser):
    return customuser.record_set.filter(status='r')

@register.filter
def users_with_books(customuser_list):
    user_list = []
    for user in customuser_list:
        if user.record_set.filter(status='o').count() != 0:
            user_list.append(user)
    return user_list

@register.filter
def books_of_user(customuser_list, user):
    books = []
    for rec in user.record_set.all():
        if rec.status == 'o':
            books.append([rec.document, rec.due_to])

    return books
