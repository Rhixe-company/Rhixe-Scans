from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_htmx.http import trigger_client_event
from render_block import render_block_to_string
from django.conf import settings
from django_tables2 import RequestConfig
from api.apps.models import Chapter
from api.apps.forms import ChapterForm, CommentForm
from api.apps.tables import ChapterTable
from api.apps.filters import ChapterFilter
from api.users.decorators import admin_only, user_only


def chapter(request, chapter_id):
    chapter = Chapter.objects.get(pk=chapter_id)

    context = {"chapter": chapter, "commentform": CommentForm()}
    return render(request, "chapter/detail.html", context)


@user_only
@admin_only
def chapterAdmin(request):
    chapters = (
        Chapter.objects.prefetch_related("chapteritems").select_related("comic").all()
    )
    myFilter = ChapterFilter(request.GET, queryset=chapters)
    table = ChapterTable(myFilter.qs)
    RequestConfig(request, paginate={"per_page": settings.PAGINATE_BY}).configure(table)
    context = {
        "table": table,
        "filter": myFilter,
    }
    if request.htmx:
        return render(request, "partials/chapter/body.html", context)
    return render(request, "chapter/admin.html", context)


@user_only
@admin_only
def chapterAdminCreate(request):
    if request.method == "POST":
        chapterform = ChapterForm(request.POST, request.FILES)
        if chapterform.is_valid():
            chapter = chapterform.save()

            context = {
                "chapter": chapter,
            }
            html = render_block_to_string(
                "partials/chapter/createsuccess.html", "chaptercreate", context
            )
            response = HttpResponse(html)
            return trigger_client_event(response, "chapter_added")
        else:
            context = {"form": chapterform}
            html = render_block_to_string(
                "partials/chapter/create.html", "chaptercreate", context
            )
            response = HttpResponse(html)
            return response
    form = ChapterForm()
    context = {
        "form": form,
    }
    if request.htmx:
        html = render_block_to_string(
            "partials/chapter/create.html", "chaptercreate", context
        )
        response = HttpResponse(html)
        return response
    return render(request, "chapter/admincreate.html", context)


@user_only
@admin_only
def chapterAdminEdit(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    form = ChapterForm(instance=chapter)
    if request.method == "POST":
        form = ChapterForm(request.POST, request.FILES, instance=chapter)
        if form.is_valid():
            newchapter = form.save()
            form = ChapterForm(instance=newchapter)
            context = {
                "chapter": newchapter,
            }
            html = render_block_to_string(
                "partials/chapter/updatesuccess.html", "chapteredit", context
            )
            response = HttpResponse(html)
            return response
        else:
            context = {"form": form, "item": chapter}
            html = render_block_to_string(
                "partials/chapter/update.html", "chapteredit", context
            )
            response = HttpResponse(html)
            return response

    context = {"form": form, "item": chapter}
    html = render_block_to_string(
        "partials/chapter/update.html", "chapteredit", context
    )
    return HttpResponse(html)


@user_only
@admin_only
def chapterAdminDelete(request, chapter_id):
    if (
        Chapter.objects.prefetch_related("chapteritems")
        .select_related("comic")
        .filter(pk=chapter_id)
        .exists()
    ):
        if request.method == "DELETE":
            chapter = get_object_or_404(Chapter, pk=chapter_id)
            chapter.delete()
            response = HttpResponse("")
            return trigger_client_event(response, "chapter_added")
        chapter = get_object_or_404(Chapter, pk=chapter_id)
        context = {"record": chapter}
        html = render_block_to_string(
            "partials/chapter/delete.html", "chapterdelete", context
        )
        return HttpResponse(html)
