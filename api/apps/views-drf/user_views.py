from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from api.apps.filters import UserFilter
from api.apps.serializers.user import UserSerializer, MyTokenObtainPairSerializer
from api.users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListCreateAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["GET", "POST"]:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class UserCreateAPIView(APIView):
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["POST"]:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["GET", "PUT"]:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class UserDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["GET", "DELETE"]:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
