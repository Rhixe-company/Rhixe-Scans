from rest_framework import serializers

from api.apps.models import Artist


class ArtistSerializer(serializers.ModelSerializer[Artist]):
    class Meta:
        model = Artist
        fields = ("name", "id")
