import json
from pprint import pprint
from django.db.utils import IntegrityError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q

from api.apps.models import Artist
from api.apps.models import Author
from api.apps.models import Chapter
from api.apps.models import ChapterImage
from api.apps.models import ChapterImagesItem
from api.apps.models import Comic
from api.apps.models import ComicImage
from api.apps.models import ComicImagesItem
from api.apps.models import Genre
from api.apps.models import Type

User = get_user_model()


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        def save_comic():
            user = User.objects.filter(
                Q(email__iexact="admin@rhixe.company") & Q(username__iexact="adminbot"),
            ).first()
            if not user:
                user = User.objects.create_superuser(
                    email="admin@rhixe.company",
                    username="adminbot",
                    password="R4I7gcJHX",
                )
            base = settings.BASE_DIR
            comics_file = str(base / "comics.json")
            with open(comics_file) as f:
                comics_data = json.load(f)
                for c in comics_data:
                    ty = Type.objects.filter(
                        Q(name__iexact=c["type"]),
                    ).update_or_create(name=c["type"],)[0]
                    au = Author.objects.filter(
                        Q(name__iexact=c["author"]),
                    ).update_or_create(name=c["author"])[0]
                    ar = Artist.objects.filter(
                        Q(name__iexact=c["artist"]),
                    ).update_or_create(name=c["artist"])[0]

                    try:
                        co = Comic.objects.filter(
                            Q(slug__iexact=c["slug"]) & Q(title__iexact=c["title"]),
                        ).update_or_create(
                            user=user,
                            type=ty,
                            artist=ar,
                            author=au,
                            title=c["title"],
                            slug=c["slug"],
                            description=c["description"],
                            rating=c["rating"],
                            status=c["status"],
                            url=c["url"],
                            spider=c["spider"],
                            updated_at=c["updated_at"],
                            # downloaded_at=c["downloaded_at"],
                            numChapters=c["numChapters"],
                            numItems=len(c["images"]),
                            serialization=c["serialization"],
                        )[
                            0
                        ]
                        genres = c["genres"]
                        if genres:
                            for gen in genres:
                                try:
                                    ge = Genre.objects.filter(
                                        Q(name__iexact=gen),
                                    ).update_or_create(name=gen)[0]
                                    co.genres.add(ge)
                                    co.save()
                                except IntegrityError as e:
                                    pprint(
                                        f"{gen} Couldnt be saved because it already exists ,Error: {e}",
                                    )
                                    pass

                        images = c["images"]
                        if images:
                            for image in images:
                                img_file = image["path"]
                                img_url = image["url"]
                                img_status = image["status"]
                                img_checksum = image["checksum"]
                                panquery = Q(url__iexact=img_url)
                                pannquery = Q(image__iexact=img_file)

                                try:
                                    lin = ComicImage.objects.filter(
                                        panquery,
                                    ).update_or_create(
                                        url=img_url,
                                        status=img_status,
                                        checksum=img_checksum,
                                    )[
                                        0
                                    ]

                                    try:
                                        im = ComicImagesItem.objects.filter(
                                            pannquery,
                                        ).update_or_create(
                                            image=img_file,
                                            link=lin,
                                            comic=co,
                                        )[
                                            0
                                        ]
                                    except IntegrityError as e:
                                        pprint(
                                            f" {e}",
                                        )
                                        pass
                                except IntegrityError as e:

                                    title = ComicImage.objects.get(panquery).image
                                    pprint(
                                        f"{title} Couldnt be saved because it already exists, {e}",
                                    )
                                    pass

                    except IntegrityError as e:
                        pprint(
                            f"{c["slug"]} Couldnt be saved because it already exists ,Error: {e}",
                        )
                        pass
            pprint(
                {
                    "Comics": Comic.objects.all().values(),
                    "ComicsImage": ComicImage.objects.all().values(),
                    "ComicsImagesItem": ComicImagesItem.objects.all().values(),
                    "ComicsCount": Comic.objects.all().count(),
                    "ComicsImageCount": ComicImage.objects.all().count(),
                    "ComicsImagesItemCount": ComicImagesItem.objects.all().count(),
                },
            )

        def save_chapter():
            base = settings.BASE_DIR

            chapters_file = str(base / "chapters.json")
            with open(chapters_file) as f:
                chapters_data = json.load(f)
                for ch in chapters_data:
                    co = Comic.objects.get(
                        Q(slug__iexact=ch["comicslug"])
                        & Q(title__iexact=ch["comictitle"]),
                    )
                    imgs = ch["images"]
                    if co:

                        try:
                            cha = Chapter.objects.filter(
                                Q(slug__iexact=ch["chapterslug"])
                                & Q(name__iexact=ch["chaptername"])
                                & Q(title__iexact=ch.get("chaptertitle", "")),
                            ).update_or_create(
                                comic=co,
                                name=ch["chaptername"],
                                title=ch.get("chaptertitle", ""),
                                # downloaded_at=ch["downloaded_at"],
                                updated_at=ch["updated_at"],
                                slug=ch["chapterslug"],
                                url=ch["url"],
                                spider=ch["spider"],
                                numPages=len(imgs),
                            )[
                                0
                            ]

                            if imgs:
                                for img in imgs:
                                    try:
                                        pa = ChapterImage.objects.filter(
                                            Q(url__iexact=img["url"]),
                                        ).update_or_create(
                                            url=img["url"],
                                            status=img["status"],
                                            checksum=img["checksum"],
                                        )[
                                            0
                                        ]

                                        try:
                                            paa = ChapterImagesItem.objects.filter(
                                                Q(image__iexact=img["path"]),
                                            ).update_or_create(
                                                chapter=cha,
                                                comic=co,
                                                link=pa,
                                                image=img["path"],
                                            )[
                                                0
                                            ]
                                        except IntegrityError as e:
                                            pprint(
                                                f"{img["path"]} Couldnt be saved because it already exists, {e}",
                                            )
                                            pass
                                    except IntegrityError as e:
                                        pprint(
                                            f"{img["url"]} Couldnt be saved because it already exists, {e}",
                                        )
                                        pass
                        except IntegrityError as e:
                            pprint(
                                f"{ch["chapterslug"]} Couldnt be saved because it already exists, {e}",
                            )
                            pass
                    else:
                        print("Comic not Found!!")
            pprint(
                {
                    "Chapters": Chapter.objects.all().values(),
                    "ChaptersImage": ChapterImage.objects.all().values(),
                    "ChaptersImagesItem": ChapterImagesItem.objects.all().values(),
                    "ChaptersCount": Chapter.objects.all().count(),
                    "ChaptersImageCount": ChapterImage.objects.all().count(),
                    "ChaptersImagesItemCount": ChapterImagesItem.objects.all().count(),
                },
            )

        save_comic()
        save_chapter()
