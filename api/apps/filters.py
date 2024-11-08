from django import forms
import django_filters
from django.utils.translation import gettext_lazy as _
from api.apps.models import Chapter
from api.apps.models import Comic
from api.users.models import User


class ChapterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search for chapters"),
                "class": "custom_search_input",
            }
        ),
    )

    class Meta:
        model = Chapter
        fields = ("name",)


class ComicFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search for comics"),
                "class": "custom_search_input",
            }
        ),
    )

    class Meta:
        model = Comic
        fields = ("title",)


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(
        field_name="email",
        lookup_expr="icontains",
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("Search for users"),
                "class": "custom_search_input",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("email",)
