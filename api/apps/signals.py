from django.db.models.signals import pre_delete

from api.apps.models import ChapterImagesItem
from api.apps.models import ComicImagesItem


def comic_server_delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.name == "image":
            file = getattr(instance, field.name)
            if file:
                file.delete(save=False)


pre_delete.connect(comic_server_delete_files, sender=ComicImagesItem)


def chapter_server_delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.name == "image":
            file = getattr(instance, field.name)
            if file:
                file.delete(save=False)


pre_delete.connect(chapter_server_delete_files, sender=ChapterImagesItem)
