from rest_framework import serializers

from api.apps.models import Author


class AuthorSerializer(serializers.ModelSerializer[Author]):
    class Meta:
        model = Author
        fields = ("name", "id")
