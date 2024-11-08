from django.urls import path

from api.apps.views import chapter_views as views

urlpatterns = [
    path("", view=views.ChapterListCreateAPIView.as_view(), name="list"),
    path(
        "<int:chapter_id>/",
        view=views.ChapterDetailAPIView.as_view(),
        name="detail",
    ),
]
