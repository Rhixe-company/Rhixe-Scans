from django.shortcuts import render
from api.apps.filters import ComicFilter
from api.apps.models import Comic
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.utils.timezone import now
from django.utils.timezone import timedelta

from ckeditor_uploader.views import ImageUploadView
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.html import escape
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from ckeditor_uploader import utils
from ckeditor_uploader.backends import get_backend

from ckeditor_uploader.utils import storage
from ckeditor_uploader.views import get_upload_filename

import os


class ImageUploadView(generic.View):
    http_method_names = ["post"]

    def post(self, request, **kwargs):
        """
        Uploads a file and send back its URL to CKEditor.
        """
        uploaded_file = request.FILES["upload"]

        backend = get_backend()

        ck_func_num = request.GET.get("CKEditorFuncNum")
        if ck_func_num:
            ck_func_num = escape(ck_func_num)

        filewrapper = backend(storage, uploaded_file)
        allow_nonimages = getattr(settings, "CKEDITOR_ALLOW_NONIMAGE_FILES", True)
        # Throws an error when an non-image file are uploaded.
        if not filewrapper.is_image and not allow_nonimages:
            return HttpResponse(
                """
                <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '', 'Invalid file type.');
                </script>""".format(
                    ck_func_num
                )
            )

        filepath = get_upload_filename(uploaded_file.name, request)

        saved_path = filewrapper.save_as(filepath)

        url = utils.get_media_url(saved_path)

        if ck_func_num:
            # Respond with Javascript sending ckeditor upload url.
            return HttpResponse(
                """
            <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '{}');
            </script>""".format(
                    ck_func_num, url
                )
            )
        else:
            _, filename = os.path.split(saved_path)
            retdata = {"url": url, "uploaded": "1", "fileName": filename}
            return JsonResponse(retdata)


upload = csrf_exempt(ImageUploadView.as_view())


def index(request):
    monthly = Q(updated_at__gte=(now() - timedelta(days=31)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)
    weekly = Q(updated_at__gte=(now() - timedelta(days=7)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)
    feat = Q(status=Comic.ComicStatus.ONGOING) | Q(status=Comic.ComicStatus.SEASON_END)

    top = Q(rating__gte=10.0) & Q(status=Comic.ComicStatus.ONGOING) | Q(
        status=Comic.ComicStatus.SEASON_END
    )
    topqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(top)
        .order_by("-updated_at")[0:7]
    )
    featqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(feat)
        .order_by("-updated_at")[0:5]
    )
    monqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(monthly)
        .order_by("-updated_at")[0:10]
    )
    weeklyqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(weekly)
        .order_by("-updated_at")[0:10]
    )
    allqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .all()
        .order_by("-updated_at")[0:10]
    )
    queryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .all()
    )
    paginator = Paginator(queryset, settings.PAGINATE_BY)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    page_obj = paginator.get_page(page_number)
    context = {
        "comics": page_obj,
        "featcomics": featqueryset,
        "topcomics": topqueryset,
        "moncomics": monqueryset,
        "weeklycomics": weeklyqueryset,
        "allcomics": allqueryset,
    }
    if request.htmx:
        return render(request, "partials/pages/index/grids.html", context)
    return render(request, "pages/index.html", context)


def comics(request):
    monthly = Q(updated_at__gt=(now() - timedelta(days=31)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)
    weekly = Q(updated_at__gt=(now() - timedelta(days=7)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)

    monqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(monthly)
        .order_by("-updated_at")[0:10]
    )
    weeklyqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(weekly)
        .order_by("-updated_at")[0:10]
    )
    allqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .all()
        .order_by("-updated_at")[0:10]
    )
    queryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .all()
    )
    comic_filter = ComicFilter(request.GET, queryset=queryset)
    paginator = Paginator(comic_filter.qs, 20)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    page_obj = paginator.get_page(page_number)
    context = {
        "comics": page_obj,
        "moncomics": monqueryset,
        "weeklycomics": weeklyqueryset,
        "allcomics": allqueryset,
        "filter": comic_filter,
    }
    if request.htmx:
        return render(request, "partials/pages/series/grid.html", context)
    return render(request, "pages/series.html", context)


def digital(request):
    monthly = Q(updated_at__gt=(now() - timedelta(days=31)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)
    weekly = Q(updated_at__gt=(now() - timedelta(days=7)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)

    monqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(monthly)
        .order_by("-updated_at")[0:10]
    )
    weeklyqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(weekly)
        .order_by("-updated_at")[0:10]
    )
    allqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .all()
        .order_by("-updated_at")[0:10]
    )
    context = {
        "moncomics": monqueryset,
        "weeklycomics": weeklyqueryset,
        "allcomics": allqueryset,
    }
    return render(request, "pages/digital.html", context)


def privacy(request):
    monthly = Q(updated_at__gt=(now() - timedelta(days=31)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)
    weekly = Q(updated_at__gt=(now() - timedelta(days=7)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)

    monqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(monthly)
        .order_by("-updated_at")[0:10]
    )
    weeklyqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(weekly)
        .order_by("-updated_at")[0:10]
    )
    allqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .all()
        .order_by("-updated_at")[0:10]
    )
    context = {
        "moncomics": monqueryset,
        "weeklycomics": weeklyqueryset,
        "allcomics": allqueryset,
    }
    return render(request, "pages/privacy.html", context)


def terms(request):
    monthly = Q(updated_at__gt=(now() - timedelta(days=31)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)
    weekly = Q(updated_at__gt=(now() - timedelta(days=7)).date()) & Q(
        status=Comic.ComicStatus.ONGOING
    ) | Q(status=Comic.ComicStatus.SEASON_END)

    monqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(monthly)
        .order_by("-updated_at")[0:10]
    )
    weeklyqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(weekly)
        .order_by("-updated_at")[0:10]
    )
    allqueryset = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .all()
        .order_by("-updated_at")[0:10]
    )
    context = {
        "moncomics": monqueryset,
        "weeklycomics": weeklyqueryset,
        "allcomics": allqueryset,
    }
    return render(request, "pages/terms.html", context)
