from django.contrib.auth import get_user_model
from django.db.models import Q
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from django.db.utils import IntegrityError
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


class CrawlerDbPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("images"):
            if adapter.get("images") and adapter.get("title"):
                images = item.get("images")
                if images:
                    title = item["title"]
                    slug = item["slug"]
                    description = item["description"]
                    rating = item["rating"]
                    status = item["status"]
                    url = item["url"]
                    spider = item["spider"]
                    updated_at = item["updated_at"]
                    numChapters = item["numChapters"]
                    numItems = len(images)
                    serialization = item["serialization"]
                    type = item["type"]
                    author = item["author"]
                    artist = item["artist"]
                    genres = item.get("genres")
                    User = get_user_model()
                    user = User.objects.filter(
                        Q(email__iexact="admin@rhixe.company")
                        & Q(username__iexact="adminbot"),
                    ).first()
                    if not user:
                        user = User.objects.create_superuser(
                            email="admin@rhixe.company",
                            username="adminbot",
                            password="R4I7gcJHX",
                        )
                    ty = Type.objects.filter(Q(name__iexact=type)).update_or_create(
                        name=type
                    )[0]
                    au = Author.objects.filter(Q(name__iexact=author)).update_or_create(
                        name=author
                    )[0]
                    ar = Artist.objects.filter(Q(name__iexact=artist)).update_or_create(
                        name=artist
                    )[0]
                    comquery = Q(slug__iexact=slug) & Q(title__iexact=title)
                    try:
                        co = Comic.objects.filter(comquery).update_or_create(
                            user=user,
                            type=ty,
                            artist=ar,
                            author=au,
                            title=title,
                            slug=slug,
                            description=description,
                            rating=rating,
                            status=status,
                            url=url,
                            spider=spider,
                            updated_at=updated_at,
                            numChapters=numChapters,
                            numItems=numItems,
                            serialization=serialization,
                        )[0]
                        for genre in genres:
                            try:
                                ge = Genre.objects.filter(
                                    Q(name__iexact=genre)
                                ).update_or_create(name=genre,)[0]
                                co.genres.add(ge)
                                co.save()
                            except IntegrityError:

                                raise DropItem(
                                    f"ComicImageItem['genres] already exists: {item!r} "
                                )
                        for image in images:
                            img_file = image["path"]
                            img_url = image["url"]
                            img_status = image["status"]
                            img_checksum = image["checksum"]

                            try:
                                panquery = Q(url__iexact=img_url)
                                lin = ComicImage.objects.filter(
                                    panquery
                                ).update_or_create(
                                    url=img_url,
                                    status=img_status,
                                    checksum=img_checksum,
                                )[
                                    0
                                ]

                                try:
                                    pannquery = Q(image__iexact=img_file)
                                    im = ComicImagesItem.objects.filter(
                                        pannquery,
                                    ).update_or_create(
                                        image=img_file,
                                        link=lin,
                                        comic=co,
                                    )[
                                        0
                                    ]
                                except IntegrityError:

                                    raise DropItem(
                                        f"ComicImageItem Already Exists In The Database: {item!r}  ",
                                    )
                            except IntegrityError:

                                raise DropItem(
                                    f"ComicImage Already Exists In The Database: {item!r} ",
                                )
                        return item
                    except IntegrityError:

                        raise DropItem(
                            f"ComicItem Already Exists In The Database: {item!r} ",
                        )

                else:
                    raise DropItem(f"ComicImageItem has not images: {item!r}")

            if (
                adapter.get("images")
                and adapter.get("comictitle")
                and adapter.get("chaptername")
            ):
                chapterimages = item.get("images")
                if chapterimages:
                    name = item["chaptername"]
                    title = item.get("chaptertitle", "")
                    slug = item["chapterslug"]
                    url = item["url"]
                    spider = item["spider"]
                    updated_at = item["updated_at"]
                    numPages = len(chapterimages)
                    comicslug = item["comicslug"]
                    comictitle = item["comictitle"]
                    comicquery = Q(slug__iexact=comicslug) & Q(title__iexact=comictitle)
                    chapterquery = (
                        Q(slug__iexact=slug)
                        & Q(name__iexact=name)
                        & Q(title__iexact=title)
                    )

                    try:
                        comic = Comic.objects.get(comicquery)
                        try:
                            ch = Chapter.objects.filter(chapterquery).update_or_create(
                                comic=comic,
                                name=name,
                                title=title,
                                updated_at=updated_at,
                                slug=slug,
                                url=url,
                                spider=spider,
                                numPages=numPages,
                            )[0]

                            for img in chapterimages:
                                cimg_file = img["path"]
                                cimg_url = img["url"]
                                cimg_status = img["status"]
                                cimg_checksum = img["checksum"]

                                try:
                                    panelquery = Q(url__iexact=cimg_url)

                                    pa = ChapterImage.objects.filter(
                                        panelquery,
                                    ).update_or_create(
                                        url=cimg_url,
                                        status=cimg_status,
                                        checksum=cimg_checksum,
                                    )[
                                        0
                                    ]

                                    try:
                                        panellquery = Q(image__iexact=cimg_file)
                                        paa = ChapterImagesItem.objects.filter(
                                            panellquery,
                                        ).update_or_create(
                                            link=pa,
                                            chapter=ch,
                                            comic=comic,
                                            image=cimg_file,
                                        )[
                                            0
                                        ]
                                    except IntegrityError:

                                        raise DropItem(
                                            f"ChapterImageItem Already Exists In The Database: {item!r} ",
                                        )
                                except IntegrityError:

                                    raise DropItem(
                                        f"ChapterImage Already Exists In The Database: {item!r} ",
                                    )

                        except IntegrityError:

                            raise DropItem(
                                f"ChapterItem Already Exists In The Database: {item!r} ",
                            )
                        return item
                    except Comic.DoesNotExist:
                        raise DropItem(
                            f"ComicItem Does Not Exists In The Database: {item!r}",
                        )
                else:
                    raise DropItem(f"ChapterImageItem has not images: {item!r}")
        else:
            raise DropItem(f"CrawlerDbPipeline Item has a Missing field in: {item!r}")
