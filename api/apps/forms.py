from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.translation import gettext_lazy as _
from .models import Comic, Comment, Chapter, Type, Genre, Author, Artist


class ComicForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Title"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Sample Comic"),
            },
        ),
    )
    slug = forms.SlugField(
        label=_("Slug"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("sample-comic"),
            },
        ),
    )
    description = forms.CharField(
        label=_("Description"),
        widget=forms.Textarea(
            attrs={
                "rows": "4",
                "class": "custom_textarea",
                "required": True,
                "placeholder": ("Write your thoughts here..."),
            },
        ),
    )
    rating = forms.DecimalField(
        max_digits=10,
        decimal_places=1,
        label=_("Rating"),
        widget=forms.NumberInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("1.0"),
            },
        ),
    )
    status = forms.ChoiceField(
        choices=Comic.ComicStatus.choices,
        label=_("Status"),
        widget=forms.Select(
            attrs={
                "class": "custom_select_input",
                "required": True,
            },
        ),
    )

    spider = forms.CharField(
        label=_("Spider"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("asura"),
            },
        ),
    )
    serialization = forms.CharField(
        label=_("Serialization"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("-"),
            },
        ),
    )
    url = forms.URLField(
        label=_("Url"),
        widget=forms.URLInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("http://localhost"),
            },
        ),
    )
    type = forms.ModelChoiceField(
        label=_("Type"),
        queryset=Type.objects.all(),
    )
    author = forms.ModelChoiceField(
        label=_("Author"),
        queryset=Author.objects.all(),
    )
    artist = forms.ModelChoiceField(
        label=_("Artist"),
        queryset=Artist.objects.all(),
    )
    genres = forms.ModelMultipleChoiceField(
        label=_("Genres"),
        queryset=Genre.objects.all(),
    )
    numChapters = forms.CharField(
        label=_("NumChapters"),
        widget=forms.NumberInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("1"),
            },
        ),
    )
    numItems = forms.CharField(
        label=_("NumItems"),
        widget=forms.NumberInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("1"),
            },
        ),
    )

    class Meta:
        model = Comic
        fields = (
            "title",
            "slug",
            "description",
            "rating",
            "status",
            "spider",
            "url",
            "type",
            "genres",
            "artist",
            "author",
            "numChapters",
        )

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_slug(self):
        return self.cleaned_data["slug"].strip()

    def clean_description(self):
        return self.cleaned_data["description"].strip()

    def clean_rating(self):
        value = self.cleaned_data["rating"].strip()
        if value <= 0:
            err = "Rating must be greater than 0."
            self.add_error("rating", err)

        return value

    def clean_numChapters(self):
        value = self.cleaned_data["numChapters"].strip()
        if value <= 0:
            err = "NumChapters must be greater than 0."
            self.add_error("numChapters", err)

        return value

    def clean_numItems(self):
        value = self.cleaned_data["numItems"].strip()
        if value <= 0:
            err = "NumItems must be greater than 0."
            self.add_error("numItems", err)

        return value

    def clean_status(self):
        return self.cleaned_data["status"].strip()

    def clean_spider(self):
        return self.cleaned_data["spider"].strip()

    def clean_url(self):
        return self.cleaned_data["url"].strip()

    def clean_type(self):
        return self.cleaned_data["type"].strip()

    def clean_author(self):
        return self.cleaned_data["author"].strip()

    def clean_artist(self):
        return self.cleaned_data["artist"].strip()

    def clean_genres(self):
        return self.cleaned_data["genres"].strip()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class ChapterForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Title"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "placeholder": ("Beginin"),
            },
        ),
    )
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Chapter 1"),
            },
        ),
    )
    slug = forms.SlugField(
        label=_("Slug"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("chapter-1"),
            },
        ),
    )

    numPages = forms.CharField(
        label=_("NumPages"),
        widget=forms.NumberInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("1"),
            },
        ),
    )

    comic = forms.ModelChoiceField(
        label=_("Comic"),
        queryset=Comic.objects.all(),
    )
    spider = forms.CharField(
        label=_("Spider"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("asura"),
            },
        ),
    )

    url = forms.URLField(
        label=_("Url"),
        widget=forms.URLInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("http://localhost"),
            },
        ),
    )

    class Meta:
        model = Chapter
        fields = ("name", "title", "slug", "numPages", "comic", "url", "spider")

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_slug(self):
        return self.cleaned_data["slug"].strip()

    def clean_numPages(self):
        value = self.cleaned_data["numPages"].strip()
        if value <= 0:
            err = "Num_Pages must be greater than 0."
            self.add_error("numPages", err)

        return value

    def clean_comic(self):
        return self.cleaned_data["comic"].strip()

    def clean_spider(self):
        return self.cleaned_data["spider"].strip()

    def clean_url(self):
        return self.cleaned_data["url"].strip()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class CommentForm(forms.ModelForm):
    """Custom storage for django_ckeditor_5 images."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].required = False

    class Meta:
        model = Comment
        fields = ("chapter", "body")
        widgets = {
            "body": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5",
                    "name": "message",
                    "required": True,
                },
                config_name="comment",
            ),
        }
