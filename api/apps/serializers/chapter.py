from rest_framework import serializers

from api.apps.models import Chapter
from api.apps.serializers.chapterimage import ChapterImageItemSerializer


class ChaptersSerializer(serializers.ModelSerializer[Chapter]):
    comictitle = serializers.CharField(source="comic.title")
    comicid = serializers.IntegerField(source="comic.id")

    class Meta:
        model = Chapter
        fields = (
            "id",
            "uuid",
            "name",
            "title",
            "slug",
            "spider",
            "url",
            "numPages",
            "updated_at",
            "comicid",
            "comictitle",
        )

    def validate_numPages(self, value):
        if value <= 0:
            err = "Num_Pages must be greater than 0."
            raise serializers.ValidationError(err)
        return value


class ChapterSerializer(serializers.ModelSerializer[Chapter]):
    chapteritems = ChapterImageItemSerializer(many=True, read_only=True)
    comictitle = serializers.CharField(source="comic.title")
    comicid = serializers.IntegerField(source="comic.id")
    chapters = serializers.SerializerMethodField(
        read_only=True,
        method_name="load_chapters",
    )

    def load_chapters(self, obj):
        chapters = obj.comic.comicchapters.all()
        serializer = ChaptersSerializer(chapters, many=True)
        return serializer.data

    class Meta:
        model = Chapter
        fields = (
            "id",
            "uuid",
            "name",
            "title",
            "slug",
            "spider",
            "url",
            "numPages",
            "updated_at",
            "comicid",
            "comictitle",
            "chapteritems",
            "chapters",
        )

    def validate_numPages(self, value):
        if value <= 0:
            err = "Num_Pages must be greater than 0."
            raise serializers.ValidationError(err)
        return value
