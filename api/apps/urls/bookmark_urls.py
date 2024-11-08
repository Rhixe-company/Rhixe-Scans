from django.urls import path

from api.apps.views import bookmark_views as views

app_name = "bookmarks"
urlpatterns = [
    path(
        "",
        view=views.bookmarks,
        name="list",
    ),
    path(
        "load/",
        view=views.loadbookmarks,
        name="load",
    ),
    path(
        "add/",
        view=views.add_bookmark,
        name="add",
    ),
    path(
        "delete/<int:comic_id>/",
        view=views.delete_bookmark,
        name="delete",
    ),
]
