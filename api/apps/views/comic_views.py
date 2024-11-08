from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_htmx.http import trigger_client_event
from render_block import render_block_to_string
from django.conf import settings
from django_tables2 import RequestConfig
from api.apps.models import Comic, UsersItem
from api.apps.forms import ComicForm
from api.apps.tables import ComicTable
from api.apps.filters import ComicFilter
from api.users.decorators import admin_only, user_only


def comic(request, comic_id):
    comic = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .get(pk=comic_id)
    )
    fav = bool
    if request.user.is_authenticated:
        if UsersItem.objects.filter(comic=comic, user=request.user).exists():
            fav = True
    context = {"fav": fav, "comic": comic}
    return render(request, "comic/detail.html", context)


@user_only
@admin_only
def comicAdmin(request):
    comics = (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .all()
    )
    myFilter = ComicFilter(request.GET, queryset=comics)
    table = ComicTable(myFilter.qs)
    RequestConfig(request, paginate={"per_page": settings.PAGINATE_BY}).configure(table)
    context = {
        "table": table,
        "filter": myFilter,
    }
    if request.htmx:
        return render(request, "partials/comic/body.html", context)
    return render(request, "comic/admin.html", context)


@user_only
@admin_only
def comicAdminCreate(request):
    if request.method == "POST":
        comicform = ComicForm(request.POST, request.FILES)
        if comicform.is_valid():
            comic = comicform.save()

            context = {
                "comic": comic,
            }
            html = render_block_to_string(
                "partials/comic/createsuccess.html", "comiccreate", context
            )
            response = HttpResponse(html)
            return trigger_client_event(response, "comic_added")
        else:
            context = {"form": comicform}
            html = render_block_to_string(
                "partials/comic/create.html", "comiccreate", context
            )
            response = HttpResponse(html)
            return response
    form = ComicForm()
    context = {
        "form": form,
    }
    if request.htmx:
        html = render_block_to_string(
            "partials/comic/create.html", "comiccreate", context
        )
        response = HttpResponse(html)
        return response
    return render(request, "comic/admincreate.html", context)


@user_only
@admin_only
def comicAdminEdit(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    form = ComicForm(instance=comic)
    if request.method == "POST":
        form = ComicForm(request.POST, request.FILES, instance=comic)
        if form.is_valid():
            newcomic = form.save()
            form = ComicForm(instance=newcomic)
            context = {
                "comic": newcomic,
            }
            html = render_block_to_string(
                "partials/comic/updatesuccess.html", "comicedit", context
            )
            response = HttpResponse(html)
            return response
        else:
            context = {"form": form, "item": comic}
            html = render_block_to_string(
                "partials/comic/update.html", "comicedit", context
            )
            response = HttpResponse(html)
            return response

    context = {"form": form, "item": comic}
    html = render_block_to_string("partials/comic/update.html", "comicedit", context)
    return HttpResponse(html)


@user_only
@admin_only
def comicAdminDelete(request, comic_id):
    if (
        Comic.objects.prefetch_related(
            "comicitems", "genres", "followers", "comicchapters"
        )
        .select_related("user", "author", "type", "artist")
        .filter(pk=comic_id)
        .exists()
    ):
        if request.method == "DELETE":
            comic = get_object_or_404(Comic, pk=comic_id)
            comic.delete()
            response = HttpResponse("")
            return trigger_client_event(response, "comic_added")
        comic = get_object_or_404(Comic, pk=comic_id)
        context = {"record": comic}
        html = render_block_to_string(
            "partials/comic/delete.html", "comicdelete", context
        )
        return HttpResponse(html)
