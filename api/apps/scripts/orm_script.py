from pprint import pprint
from django.db.models import Q
from django.utils.timezone import now
from django.utils.timezone import timedelta

from api.apps.models import Comic


def run():

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
    context = {
        "comics": queryset,
        "featcomics": featqueryset,
        "topcomics": topqueryset,
        "moncomics": monqueryset,
        "weeklycomics": weeklyqueryset,
        "allcomics": allqueryset,
    }
    context2 = {
        "comics-count": queryset.count(),
        "featcomics-count": featqueryset.count(),
        "topcomics-count": topqueryset.count(),
        "moncomics-count": monqueryset.count(),
        "weeklycomics-count": weeklyqueryset.count(),
        "allcomics-count": allqueryset.count(),
    }
    pprint(context)
    pprint(context2)
