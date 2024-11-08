from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.apps"
    verbose_name = _("Apps")

    def ready(self):
        pass
