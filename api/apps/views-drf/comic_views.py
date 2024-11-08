from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.utils.timezone import now
from django.utils.timezone import timedelta

# from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.apps.filters import ComicFilter
from api.apps.models import Comic
from api.apps.serializers.comic import ComicSerializer, ComicsSerializer


class ComicListCreateAPIView(generics.ListCreateAPIView):
    queryset = (
        Comic.objects.prefetch_related(
            "comicitems",
            "genres",
            "followers",
            "comicchapters",
        )
        .select_related("user", "author", "type", "artist")
        .all()
    )
    serializer_class = ComicsSerializer
    filterset_class = ComicFilter

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ComicDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        Comic.objects.prefetch_related(
            "comicitems",
            "genres",
            "followers",
            "comicchapters",
        )
        .select_related("user", "author", "type", "artist")
        .all()
    )
    serializer_class = ComicSerializer
    lookup_url_kwarg = "comic_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ComicTopAPIView(generics.ListAPIView):
    pagination_class = None
    daily = (now() - timedelta(days=1)).date()
    top = Q(numItems=2) & Q(rating__gte=10.0)
    queryset = (
        Comic.objects.prefetch_related(
            "comicitems",
            "genres",
            "followers",
            "comicchapters",
        )
        .select_related("user", "author", "type", "artist")
        .filter(top)
        .order_by("-rating")[0:7]
    )
    serializer_class = ComicsSerializer
