from django.shortcuts import render
from api.apps.models import Comic, UsersItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.utils.timezone import now
from django.utils.timezone import timedelta
from django.http import HttpResponse
from render_block import render_block_to_string
from api.users.decorators import user_only
from django.views.decorators.http import require_http_methods
from api.apps.utils import get_max_order, reorder
from django_htmx.http import trigger_client_event


@user_only
def bookmarks(request):
    comics = UsersItem.objects.prefetch_related("comic").filter(user=request.user)
    paginator = Paginator(comics, 20)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    page_obj = paginator.get_page(page_number)
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
        "comics": page_obj,
        "moncomics": monqueryset,
        "weeklycomics": weeklyqueryset,
        "allcomics": allqueryset,
    }
    if request.htmx:
        return render(request, "partials/bookmark/grid.html", context)
    return render(request, "bookmark/list.html", context)


def loadbookmarks(request):
    comics = UsersItem.objects.prefetch_related("comic").filter(user=request.user)

    context = {
        "items": comics,
    }

    html = render_block_to_string("partials/bookmarks.html", "comicbookmark", context)
    response = HttpResponse(html)
    return response


def countbookmarks(request):
    comics = UsersItem.objects.prefetch_related("comic").filter(user=request.user)

    context = {
        "items": comics,
    }

    html = render_block_to_string("partials/book_count.html", "comicbookmark", context)
    response = HttpResponse(html)
    return response


@require_http_methods(["POST", "GET"])
@user_only
def add_bookmark(request):
    title = request.POST.get("comictitle")

    # add comic
    comic = Comic.objects.get(Q(title__iexact=title))

    if not UsersItem.objects.filter(comic=comic, user=request.user).exists():

        UsersItem.objects.create(
            comic=comic, user=request.user, order=get_max_order(request.user)
        )
    context = {"comic": comic}
    html = render_block_to_string(
        "partials/comic/addbutton.html", "comicbookmark", context
    )
    response = HttpResponse(html)

    return trigger_client_event(response, "comic_bookmark")


@require_http_methods(["POST", "GET"])
@user_only
def delete_bookmark(request, comic_id):
    # remove the comic from the user's list
    UsersItem.objects.get(comic=comic_id).delete()
    comic = Comic.objects.get(id=comic_id)
    reorder(request.user)
    context = {"comic": comic}
    html = render_block_to_string(
        "partials/comic/removebutton.html", "comicbookmark", context
    )
    response = HttpResponse(html)
    return trigger_client_event(response, "comic_bookmark")
