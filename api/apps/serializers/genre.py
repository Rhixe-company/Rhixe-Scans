from rest_framework import serializers

from api.apps.models import Genre


class GenreSerializer(serializers.ModelSerializer[Genre]):
    class Meta:
        model = Genre
        fields = ("name", "id")
