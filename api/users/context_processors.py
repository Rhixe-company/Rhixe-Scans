from django.conf import settings
from django.db.models import Q
from .models import User

# from django.contrib import messages


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user)

        avatar = User.objects.filter(email=user)

        context = {
            "avatar": avatar,
        }
        return context
    return {"NotLoggedIn": User.objects.none()}
