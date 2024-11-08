from django.urls import path

from api.apps.views import chapter_views as views

app_name = "chapters"
urlpatterns = [
    path(
        "<int:chapter_id>/",
        view=views.chapter,
        name="chapter_detail",
    ),
    path(
        "admin/",
        view=views.chapterAdmin,
        name="admin",
    ),
    path(
        "admin/create/",
        view=views.chapterAdminCreate,
        name="admin_create",
    ),
    path(
        "admin/edit/<int:chapter_id>/",
        view=views.chapterAdminEdit,
        name="admin_edit",
    ),
    path(
        "admin/delete/<int:chapter_id>/",
        view=views.chapterAdminDelete,
        name="admin_delete",
    ),
]
