from rest_framework import generics
from rest_framework.permissions import AllowAny

# from rest_framework.permissions import IsAdminUser
from api.apps.filters import ChapterFilter
from api.apps.models import Chapter
from api.apps.serializers.chapter import ChapterSerializer
from api.apps.serializers.chapter import ChaptersSerializer


class ChapterListCreateAPIView(generics.ListCreateAPIView):
    queryset = (
        Chapter.objects.prefetch_related("chapteritems").select_related("comic").all()
    )
    serializer_class = ChaptersSerializer
    filterset_class = ChapterFilter

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ChapterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        Chapter.objects.prefetch_related("chapteritems").select_related("comic").all()
    )
    serializer_class = ChapterSerializer
    lookup_url_kwarg = "chapter_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
