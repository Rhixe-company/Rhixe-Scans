from django.urls import path


from . import views

app_name = "users"
urlpatterns = [
    path("~redirect/", view=views.user_redirect_view, name="redirect"),
    path("update/<int:pk>/", view=views.user_update_view, name="update"),
    path("<int:pk>/", view=views.user_detail_view, name="detail"),
    path(
        "admin/",
        view=views.userAdmin,
        name="admin",
    ),
    path(
        "admin/create/",
        view=views.userAdminCreate,
        name="admin_create",
    ),
    path(
        "admin/edit/<int:user_id>/",
        view=views.userAdminEdit,
        name="admin_edit",
    ),
    path(
        "admin/delete/<int:user_id>/",
        view=views.userAdminDelete,
        name="admin_delete",
    ),
]
