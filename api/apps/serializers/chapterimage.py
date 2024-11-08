from rest_framework import serializers

from api.apps.models import ChapterImage
from api.apps.models import ChapterImagesItem


class ChapterImageSerializer(serializers.ModelSerializer[ChapterImage]):
    class Meta:
        model = ChapterImage
        fields = (
            "url",
            "status",
            "checksum",
        )


class ChapterImageItemSerializer(serializers.ModelSerializer[ChapterImagesItem]):
    class Meta:
        model = ChapterImagesItem
        fields = (
            "image",
            "link",
            "chapter",
            "comic",
        )
