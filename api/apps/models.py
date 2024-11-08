# models.py
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from api.apps.managers import NewManager

User = get_user_model()

ext_validator = FileExtensionValidator(
    [
        "ico",
        "jpg",
        "svg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "webp",
        "tiff",
        "ttf",
        "eot",
        "woff",
        "woff2",
    ],
)


def panel_location(instance, filename):
    return "{}/{}/{}".format(
        str(instance.comic.slug)
        .replace(" ", "_")
        .replace(":", " ")
        .replace("/", "")
        .replace("\\", ""),
        instance.chapter.slug,
        filename,
    )


def comic_location(instance, filename):
    return "{}/{}".format(
        str(instance.comic.slug)
        .replace(" ", "_")
        .replace(":", " ")
        .replace("/", "")
        .replace("\\", ""),
        filename,
    )


class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Genres"
        verbose_name = "Genre"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Authors"
        verbose_name = "Author"

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Artists"
        verbose_name = "Artist"

    def __str__(self):
        return self.name


class Type(models.Model):
    class TypeStatus(models.TextChoices):
        MANGA = "Manga"
        MANHWA = "Manhwa"
        MANHUA = "Manhua"

    name = models.CharField(
        _("Name"),
        max_length=6,
        choices=TypeStatus.choices,
    )

    class Meta:
        verbose_name_plural = "Types"
        verbose_name = "Type"

    def __str__(self):
        return self.name


class ComicImage(models.Model):
    class ComicImageStatus(models.TextChoices):
        UPTODATE = "uptodate"
        DOWNLOADED = "downloaded"

    url = models.URLField(_("Url"), unique=True, max_length=500)
    checksum = models.CharField(_("Checksum"), max_length=500, blank=True)
    status = models.CharField(
        _("Status"),
        max_length=11,
        choices=ComicImageStatus.choices,
        default="downloaded",
    )

    def __str__(self):
        return self.url


class Comic(models.Model):
    class ComicStatus(models.TextChoices):
        COMPLETED = "Completed"
        ONGOING = "Ongoing"
        HIATUS = "Hiatus"
        DROPPED = "Dropped"
        SEASON_END = "Season End"
        COMING_SOON = "Coming Soon"

    uuid = models.UUIDField(_("Uuid"), default=uuid.uuid4, editable=False)
    title = models.CharField(_("Title"), max_length=500, unique=True)
    slug = models.SlugField(_("Slug"), max_length=500, unique=True)
    description = models.TextField(_("Description"))
    status = models.CharField(
        _("Status"),
        max_length=15,
        choices=ComicStatus.choices,
    )
    rating = models.DecimalField(_("Rating"), max_digits=10, decimal_places=1)
    serialization = models.CharField(
        _("Serialization"),
        max_length=500,
        blank=True,
    )
    numChapters = models.PositiveIntegerField(_("Total Chapters"))
    spider = models.CharField(_("Spider"), max_length=500)
    url = models.URLField(_("Url"), max_length=500)
    numItems = models.PositiveSmallIntegerField(_("Total Items"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="comictype")
    genres = models.ManyToManyField(Genre, blank=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        blank=True,
        related_name="comicauthor",
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        blank=True,
        related_name="comicartist",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comicuser",
    )
    users = models.ManyToManyField(
        User,
        through="UsersItem",
        blank=True,
    )
    images = models.ManyToManyField(ComicImage, through="ComicImagesItem")

    objects = NewManager.as_manager()

    class Meta:
        verbose_name_plural = "Comics"
        verbose_name = "Comic"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def has_items(self):
        return self.numItems > 1

    def get_absolute_url(self) -> str:
        return reverse("comics:comic_detail", kwargs={"comic_id": self.pk})


class ComicImagesItem(models.Model):
    link = models.ForeignKey(ComicImage, on_delete=models.CASCADE)
    comic = models.ForeignKey(
        Comic,
        on_delete=models.CASCADE,
        related_name="comicitems",
    )
    image = models.ImageField(
        _("Image"),
        upload_to=comic_location,
        validators=[
            ext_validator,
        ],
        max_length=500,
    )

    def __str__(self):
        return f"{self.image}"

    def save(self, *args, **kwargs):
        if self.pk:
            existing = get_object_or_404(ComicImagesItem, pk=self.pk)
            if existing.image != self.image:
                existing.image.delete(save=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)


class UsersItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name="followers")
    order = models.PositiveSmallIntegerField(
        _("Order"),
    )

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "UsersItems"
        verbose_name = "Usersitem"

    def __str__(self):
        return (
            f"Order - {self.order} User - {self.user.email} Comic - {self.comic.title}"
        )


class ChapterImage(models.Model):
    class ChapterImageStatus(models.TextChoices):
        UPTODATE = "uptodate"
        DOWNLOADED = "downloaded"

    url = models.URLField(_("Url"), unique=True, max_length=500)
    checksum = models.CharField(_("Checksum"), max_length=500, blank=True)
    status = models.CharField(
        _("Status"),
        max_length=11,
        choices=ChapterImageStatus.choices,
        default="downloaded",
    )

    def __str__(self):
        return self.url


class Chapter(models.Model):
    uuid = models.UUIDField(_("Uuid"), default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=500)
    title = models.CharField(_("Title"), max_length=500, blank=True, null=True)
    slug = models.SlugField(_("Slug"), max_length=500, unique=True)
    spider = models.CharField(_("Spider"), max_length=500)
    url = models.URLField(_("Url"), max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(
        blank=True,
    )
    numPages = models.PositiveSmallIntegerField(_("Total Pages"))
    comic = models.ForeignKey(
        Comic,
        on_delete=models.CASCADE,
        related_name="comicchapters",
    )
    images = models.ManyToManyField(ChapterImage, through="ChapterImagesItem")

    class Meta:
        verbose_name_plural = "Chapters"
        verbose_name = "Chapter"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def has_pages(self):
        return self.numPages > 0

    def get_absolute_url(self) -> str:
        return reverse("chapters:chapter_detail", kwargs={"chapter_id": self.pk})


class ChapterImagesItem(models.Model):
    link = models.ForeignKey(ChapterImage, on_delete=models.CASCADE)
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="chapteritems",
    )
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    image = models.ImageField(
        _("Image"),
        upload_to=panel_location,
        validators=[ext_validator],
        max_length=500,
    )

    def __str__(self):
        return f"{self.image}"

    def save(self, *args, **kwargs):
        if self.pk:
            existing = get_object_or_404(ChapterImagesItem, pk=self.pk)
            if existing.image != self.image:
                existing.image.delete(save=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)


class Comment(models.Model):
    body = CKEditor5Field(_("Body"), config_name="extends")
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="chaptercomments",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="usercomments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Comments"
        verbose_name = "Comment"

    def __str__(self):
        return f"{self.body}"
