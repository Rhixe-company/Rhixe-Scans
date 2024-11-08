from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from api.apps.models import UsersItem
from api.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "images",
            "is_staff",
        )


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "images",
            "is_staff",
            "token",
        ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class UsersItemSerializer(serializers.ModelSerializer[UsersItem]):
    user = UserSerializer(many=False, read_only=False)

    class Meta:
        model = UsersItem
        fields = ("user", "comic", "order")
