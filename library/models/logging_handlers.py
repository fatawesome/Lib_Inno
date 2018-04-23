from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from utils.logging import log_addition_user, log_addition_queue, log_addition_record, log_addition_document
from utils.logging import log_deletion_user, log_deletion_queue, log_deletion_record, log_deletion_document
from utils.logging import log_change_user, log_change_queue, log_change_record, log_change_document

from .documents import Document
from .record import Record
from login.models import CustomUser
from .request_queue import RequestQueueElement


# RequestQueue handlers

@receiver(post_save, sender=RequestQueueElement)
def post_save_queue_handler(sender, instance, created, using, **kwargs):
    print("!!!!!!!!!!!!!!!!! IM HERE !!!!!!!!!!!!!!!")
    if isinstance(instance, RequestQueueElement):
        if created:
            log_addition_queue(instance)
        else:
            log_change_queue(instance)


@receiver(post_delete, sender=RequestQueueElement)
def post_delete_queue_handler(sender, instance, using, **kwargs):
    if isinstance(instance, RequestQueueElement):
        log_deletion_queue(instance)


# CustomUser handlers

@receiver(post_save, sender=CustomUser)
def post_save_user_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, CustomUser):
        if created:
            log_addition_user(instance)
        else:
            log_change_user(instance)


@receiver(post_delete, sender=CustomUser)
def post_delete_user_handler(sender, instance, using, **kwargs):
    if isinstance(instance, CustomUser):
        log_deletion_user(instance)


# Document handlers

@receiver(post_save, sender=Document)
def post_save_document_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Document):
        if created:
            log_addition_document(instance)
        else:
            log_change_document(instance)


@receiver(post_delete, sender=Document)
def post_delete_document_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Document):
        log_deletion_document(instance)


# Record handlers

@receiver(post_save, sender=Record)
def post_save_record_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Record):
        if created:
            log_addition_record(instance)
        else:
            log_change_record(instance)


@receiver(post_delete, sender=Record)
def post_delete_record_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Record):
        log_deletion_record(instance)
