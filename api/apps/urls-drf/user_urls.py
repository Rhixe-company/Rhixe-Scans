from django.urls import path

from api.apps.views import user_views as views


urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("", view=views.UserListCreateAPIView.as_view(), name="list"),
    path("create/", view=views.UserCreateAPIView.as_view(), name="create"),
    path("<int:user_id>/", view=views.UserDetailAPIView.as_view(), name="detail"),
    path(
        "<int:user_id>/update/", view=views.UserUpdateAPIView.as_view(), name="update"
    ),
    path(
        "<int:user_id>/delete/", view=views.UserDestroyAPIView.as_view(), name="delete"
    ),
]
