# # storage.py
# import hashlib

# from django.core.files.storage import Storage


# class DuplicateAwareStorage(Storage):
#     def _save(self, name, content):
#         content_hash = hashlib.md5(content.read()).hexdigest()
#         existing_file = self.exists(name)
#         if existing_file:
#             if self.get_available_name(name).split(".")[0] == content_hash:
#                 # File is a duplicate, use the existing one
#                 return existing_file
#         # Upload the new file
#         # ...
#         return name
import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CustomStorage(FileSystemStorage):
    """Custom storage for django_ckeditor_5 images."""

    location = os.path.join(settings.MEDIA_ROOT, "django_ckeditor_5")
    base_url = urljoin(settings.MEDIA_URL, "django_ckeditor_5/")
