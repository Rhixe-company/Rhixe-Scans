from django.urls import path

from api.apps.views import comic_views as views

app_name = "comics"
urlpatterns = [
    path(
        "<int:comic_id>/",
        view=views.comic,
        name="comic_detail",
    ),
    path(
        "admin/",
        view=views.comicAdmin,
        name="admin",
    ),
    path(
        "admin/create/",
        view=views.comicAdminCreate,
        name="admin_create",
    ),
    path(
        "admin/edit/<int:comic_id>/",
        view=views.comicAdminEdit,
        name="admin_edit",
    ),
    path(
        "admin/delete/<int:comic_id>/",
        view=views.comicAdminDelete,
        name="admin_delete",
    ),
]
