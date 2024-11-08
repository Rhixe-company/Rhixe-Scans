from rest_framework import serializers

from api.apps.models import ComicImage
from api.apps.models import ComicImagesItem


class ComicImageItemSerializer(serializers.ModelSerializer[ComicImagesItem]):
    class Meta:
        model = ComicImagesItem
        fields = (
            "image",
            "link",
            "comic",
        )


class ComicImageSerializer(serializers.ModelSerializer[ComicImage]):
    class Meta:
        model = ComicImage
        fields = (
            "url",
            "status",
            "checksum",
        )
