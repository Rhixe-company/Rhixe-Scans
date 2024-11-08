from django.urls import path

from api.apps.views import comic_views as views

urlpatterns = [
    path("", view=views.ComicListCreateAPIView.as_view(), name="comiclist"),
    path("top/", view=views.ComicTopAPIView.as_view(), name="comictop"),
    path(
        "<int:comic_id>/",
        view=views.ComicDetailAPIView.as_view(),
        name="comicdetail",
    ),
]
