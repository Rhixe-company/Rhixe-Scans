from rest_framework import serializers

from api.apps.models import Comic
from api.apps.serializers.artist import ArtistSerializer
from api.apps.serializers.author import AuthorSerializer
from api.apps.serializers.chapter import ChaptersSerializer
from api.apps.serializers.comicimage import ComicImageItemSerializer
from api.apps.serializers.genre import GenreSerializer
from api.apps.serializers.type import TypeSerializer
from api.apps.serializers.user import UserSerializer
from api.apps.serializers.user import UsersItemSerializer


class ComicSerializer(serializers.ModelSerializer[Comic]):
    comicitems = ComicImageItemSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    followers = UsersItemSerializer(many=True, read_only=True)
    type = TypeSerializer(many=False, read_only=True)
    author = AuthorSerializer(many=False, read_only=True)
    artist = ArtistSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    comicchapters = ChaptersSerializer(many=True, read_only=True)
    # chapters = serializers.SerializerMethodField(
    #     read_only=True, method_name="load_chapters"
    # )

    # def load_chapters(self, obj):
    #     chapters = obj.chapters.all()
    #     serializer = ChapterSerializer(chapters, many=True)
    #     return serializer.data

    class Meta:
        model = Comic
        fields = (
            "id",
            "uuid",
            "title",
            "slug",
            "status",
            "description",
            "rating",
            "spider",
            "url",
            "serialization",
            "numChapters",
            "updated_at",
            "comicitems",
            "type",
            "author",
            "artist",
            "user",
            "genres",
            "followers",
            "comicchapters",
        )

    def validate_numChapters(self, value):
        if value <= 0:
            err = "Num_Chapters must be greater than 0."
            raise serializers.ValidationError(err)
        return value


class ComicsSerializer(serializers.ModelSerializer[Comic]):
    comicitems = ComicImageItemSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    followers = UsersItemSerializer(many=True, read_only=True)
    type = TypeSerializer(many=False, read_only=True)
    author = AuthorSerializer(many=False, read_only=True)
    artist = ArtistSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    chapters = serializers.SerializerMethodField(
        read_only=True,
        method_name="load_chapters",
    )

    def load_chapters(self, obj):
        chapters = obj.comicchapters.all()[0:3]
        serializer = ChaptersSerializer(chapters, many=True)
        return serializer.data

    class Meta:
        model = Comic
        fields = (
            "id",
            "uuid",
            "title",
            "slug",
            "status",
            "description",
            "rating",
            "spider",
            "url",
            "serialization",
            "numChapters",
            "updated_at",
            "comicitems",
            "type",
            "author",
            "artist",
            "user",
            "genres",
            "followers",
            "chapters",
        )

    def validate_numChapters(self, value):
        if value <= 0:
            err = "Num_Chapters must be greater than 0."
            raise serializers.ValidationError(err)
        return value
