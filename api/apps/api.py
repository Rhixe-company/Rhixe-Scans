from django.urls import path, include


urlpatterns = [
    path("users/", include("api.apps.urls.user_urls")),
    path("comics/", include("api.apps.urls.comic_urls")),
    path("chapters/", include("api.apps.urls.chapter_urls")),
]
