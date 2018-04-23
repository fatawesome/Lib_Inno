import datetime

from background_task import background
from background_task.models import Task
from django.core.mail import send_mail

from library.models import Document
from library.views import send_mail_document_reserved_by_user, update_request_queue


@background(schedule=1)
def update_reserved_documents():
    print("Hello")
    for doc in Document.objects.all():
        if doc.requestqueueelement_set.all().count() != 0:
            for rec in doc.record_set.filter(status='r'):
                if rec.due_to == None:
                    rec.due_to = datetime.date.today() + datetime.timedelta(days=1)
                    rec.save()
                    send_mail_document_reserved_by_user(rec.user, rec.document, True)
                elif datetime.date.today() > rec.due_to:
                    send_mail(
                        'You did not take the document',
                        'You didn\'t take the document "' + doc.title + '" from the library. Reserve withdrawn. You can try to reserve it again. ' + '\n\n\n\n-------\nBest regards, \nLibInno \nLibrary managment system',
                        'fatawesomeee@yandex.ru',
                        [rec.user.email],
                        fail_silently=False
                    )
                    rec.make_available()
                update_request_queue(rec.document)


# if Task.objects.filter(task_name='library.tasks.update_reserved_documents').count() == 0:
#    update_reserved_documents(repeat=24 * 60 * 60)  # repeat daily
