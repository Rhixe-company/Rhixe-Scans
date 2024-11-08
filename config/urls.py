# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from . import views

# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularRedocView,
#     SpectacularSwaggerView,
# )

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path("", view=views.index, name="index"),
    path("comics/", view=views.comics, name="comics"),
    path(
        "digital/",
        view=views.digital,
        name="digital",
    ),
    path(
        "privacy/",
        view=views.privacy,
        name="privacy",
    ),
    path(
        "terms/",
        view=views.terms,
        name="terms",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("api.users.urls", namespace="users")),
    # Comic management
    path("comics/", include("api.apps.urls.comic_urls", namespace="comics")),
    # Chapter management
    path("chapters/", include("api.apps.urls.chapter_urls", namespace="chapters")),
    # Bookmark management
    path("bookmarks/", include("api.apps.urls.bookmark_urls", namespace="bookmarks")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("allauth.socialaccount.urls")),
    path("captcha/", include("captcha.urls")),
    # path("ckeditor5/", include("ckeditor_uploader.urls")),
    path("upload/", views.upload, name="custom_upload_file"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # API URLS
# urlpatterns += [
#     # API base url
#     path("api/", include("api.apps.api")),
#     # # DRF auth token
#     # path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
#     # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
#     # Optional UI:
#     path(
#         "api/schema/swagger-ui/",
#         SpectacularSwaggerView.as_view(url_name="schema"),
#         name="swagger-ui",
#     ),
#     path(
#         "api/schema/redoc/",
#         SpectacularRedocView.as_view(url_name="schema"),
#         name="redoc",
#     ),
# ]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
