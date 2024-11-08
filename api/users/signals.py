from django.db.models.signals import pre_delete
from django.dispatch import receiver

from api.users.models import User


@receiver(pre_delete, sender="users.User")
def user_server_delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.name == "images":
            file = getattr(instance, field.name)
            if file:
                file.delete(save=False)


pre_delete.connect(user_server_delete_files, sender=User)
