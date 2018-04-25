from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from utils.logging import log_change, log_addition, log_delete, log_email

from .documents import Document, Book, Article, Audio, Video
from .tag import Tag
from .author import Author
from .record import Record
from login.models import CustomUser
from .request_queue import RequestQueueElement


# RequestQueue handlers

@receiver(post_save, sender=RequestQueueElement)
def post_save_queue_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, RequestQueueElement):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=RequestQueueElement)
def post_delete_queue_handler(sender, instance, using, **kwargs):
    if isinstance(instance, RequestQueueElement):
        log_delete(instance)


# CustomUser handlers

@receiver(post_save, sender=CustomUser)
def post_save_user_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, CustomUser):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=CustomUser)
def post_delete_user_handler(sender, instance, using, **kwargs):
    if isinstance(instance, CustomUser):
        log_delete(instance)


# Book handlers

@receiver(post_save, sender=Book)
def post_save_book_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Book):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=Book)
def post_delete_book_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Book):
        log_delete(instance)


# Article handlers

@receiver(post_save, sender=Article)
def post_save_article_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Article):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=Article)
def post_delete_article_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Article):
        log_delete(instance)


# Audio handlers

@receiver(post_save, sender=Audio)
def post_save_audio_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Audio):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=Audio)
def post_delete_audio_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Audio):
        log_delete(instance)


# Video handlers

@receiver(post_save, sender=Video)
def post_save_video_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Video):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=Video)
def post_delete_video_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Video):
        log_delete(instance)


# Record handlers

@receiver(post_save, sender=Record)
def post_save_record_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Record):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=Record)
def post_delete_record_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Record):
        log_delete(instance)


# Tag handlers

@receiver(post_save, sender=Tag)
def post_save_tag_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Tag):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=Tag)
def post_delete_tag_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Tag):
        log_delete(instance)


# Author handlers

@receiver(post_save, sender=Author)
def post_save_author_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, Author):
        if created:
            log_addition(instance)
        else:
            log_change(instance)


@receiver(post_delete, sender=Author)
def post_delete_author_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Author):
        log_delete(instance)
