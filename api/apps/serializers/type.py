from rest_framework import serializers

from api.apps.models import Type


class TypeSerializer(serializers.ModelSerializer[Type]):
    class Meta:
        model = Type
        fields = ("name", "id")
