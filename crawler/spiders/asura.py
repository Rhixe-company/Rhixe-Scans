import logging

from scrapy import Spider
from scrapy.loader import ItemLoader

from crawler.items import ChapterItem
from crawler.items import ComicItem

logger = logging.getLogger(__name__)


class AsuraSpider(Spider):
    name = "asura"
    allowed_domains = ["asuracomic.net"]
    start_urls = [
        "https://asuracomic.net/series/the-dark-magician-transmigrates-after-66666-years-ac320030",
    ]
    # redis_key = "asuracomic_queue:start_urls"

    # redis_batch_size = 1

    # max_idle_time = 7

    custom_feed = {
        "comic.json": {
            "format": "json",
            "encoding": "utf8",
            "store_empty": False,
            "item_classes": ["crawler.items.ComicItem"],
            "fields": None,
            "indent": 4,
        },
        "chapter.json": {
            "format": "json",
            "encoding": "utf8",
            "store_empty": False,
            "item_classes": ["crawler.items.ChapterItem"],
            "fields": None,
            "indent": 4,
        },
    }

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.setdefault("FEEDS", {}).update(cls.custom_feed)

    def parse(self, response):
        loader = ItemLoader(item=ComicItem(), selector=response)
        loader.add_xpath(
            "title",
            "//div[@class='text-center sm:text-left']/span/text()",
        )
        loader.add_xpath(
            "slug",
            "//div[@class='text-center sm:text-left']/span/text()",
        )

        loader.add_xpath(
            "serialization",
            "//div[@class='grid grid-cols-1 md:grid-cols-2 gap-5 mt-8']/div[1]/h3[2]/text()",
        )
        loader.add_xpath(
            "author",
            "//div[@class='grid grid-cols-1 md:grid-cols-2 gap-5 mt-8']/div[2]/h3[2]/text()",
        )
        loader.add_xpath(
            "artist",
            "//div[@class='grid grid-cols-1 md:grid-cols-2 gap-5 mt-8']/div[3]/h3[2]/text()",
        )
        # loader.add_xpath(
        #     "updated_at",
        #     '//div[contains(@class, "grid grid-cols-1 md:grid-cols-2 gap-5 mt-8")]/div[5]/h3[2]/text()',
        # )

        loader.add_xpath(
            "rating",
            "//div[@class='bg-[#343434] px-2 py-1 flex items-center justify-between rounded-[3px]']/p/text()",
        )
        loader.add_xpath(
            "status",
            "//div[@class='bg-[#343434] px-2 py-2 flex items-center justify-between rounded-[3px] w-full']/h3[2]/text()",
        )
        loader.add_xpath(
            "type",
            "//div[@class='bg-[#343434] px-2 py-2 flex items-center justify-between rounded-[3px] w-full'][2]/h3[2]/text()",
        )
        image = response.xpath("//img[@class='rounded mx-auto md:mx-0 ']/@src").get()
        image2 = response.xpath(
            '//div[contains(@class, "bigcover")]/img[contains(@data-nimg, "1")]/@src',
        ).get()

        chapters = response.xpath(
            '//div[contains(@class, "pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20 relative")]/h3/a/@href',
        ).getall()[0:1]
        chapters_time = response.xpath(
            '//div[contains(@class, "pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20 relative")]/h3[2]/text()',
        ).getall()[0:1]
        comic_time = response.xpath(
            '//div[contains(@class, "pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20 relative")]/h3[2]/text()',
        ).get()
        loader.add_value("updated_at", comic_time)
        loader.add_value("url", response.url)
        cimages = []
        cimages.append(response.urljoin(image))
        if image2:
            cimages.append(response.urljoin(image2))
        loader.add_value("image_urls", cimages)
        loader.add_value(
            "numChapters",
            len(chapters),
        )
        genres = response.xpath(
            "//div[@class='flex flex-row flex-wrap gap-3']/button/text()",
        ).getall()
        if not genres:
            loader.add_value(
                "genres",
                "-",
            )
        else:
            loader.add_xpath(
                "genres",
                "//div[@class='flex flex-row flex-wrap gap-3']/button/text()",
            )
        des = response.xpath(
            '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/text()',
        ).getall()
        desem = response.xpath(
            '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/strong/em/text()',
        ).getall()
        if not des:
            newdes = response.xpath(
                '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/text()',
            ).getall()
            newdesem = response.xpath(
                '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/strong/em/text()',
            ).getall()
            newdesem1 = response.xpath(
                '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/strong[1]/text()',
            ).getall()
            if not newdes:
                olddes = response.xpath(
                    '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/div/div/div[1]/text()',
                ).getall()
                if olddes:
                    oldesem = response.xpath(
                        '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/div/div/div[1]/strong/em/text()',
                    ).getall()
                    if not oldesem:

                        olddesdiv = f"{olddes}"
                        loader.add_value("description", olddesdiv)
                    else:
                        oldesemdiv = f"{olddes}{oldesem}"
                        loader.add_value("description", oldesemdiv)
            if not newdesem:
                mynewdes = f"{newdes}"
                loader.add_value("description", mynewdes)
            if not newdesem1:
                newdesem1div = f"{newdesem}{newdes}"
                loader.add_value("description", newdesem1div)
            else:
                newdesem2 = response.xpath(
                    '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/strong[2]/em/text()',
                ).getall()
                if not newdesem2:
                    newdesemdiv1 = f"{newdesem}{newdesem1}"
                    loader.add_value("description", newdesemdiv1)
                else:
                    newdesem3 = response.xpath(
                        '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/strong[2]/em/text()',
                    ).getall()
                    if not newdesem3:
                        newdesemdiv2 = f"{newdesem}{newdesem1}{newdesem2}"
                        loader.add_value("description", newdesemdiv2)
                    else:
                        newdesemdiv3 = f"{newdesem}{newdesem1}{newdesem2}{newdesem3}"
                        loader.add_value("description", newdesemdiv3)
        if not desem:
            mydes = f"{des}"
            loader.add_value("description", mydes)
        mydesem = f"{desem} {des}"
        loader.add_value("description", mydesem)

        item = loader.load_item()
        yield item

        if chapters:
            for x, y in zip(chapters, chapters_time, strict=False):
                yield response.follow(
                    x,
                    callback=self.parsechapter,
                    cb_kwargs=dict(chapters_time=y),
                )
        logger.debug("A New Comic was found at %s", response.url)

    def parsechapter(self, response, chapters_time):
        loader = ItemLoader(item=ChapterItem(), selector=response)
        images = []
        image_urls = response.xpath(
            "//div[@class='w-full mx-auto center']/img[@class='object-cover mx-auto']/@src",
        ).getall()
        for image in image_urls:
            images.append(response.urljoin(image))
        title = response.xpath(
            "//div[@class='flex flex-col items-center space-y-2 pt-6 px-5 text-center']/p/a/span/text()",
        ).get()
        chaptertitle = (
            response.xpath(
                '//div[contains(@class, "dropdown md:w-[13em] max-[350px]:w-[10rem] ")]/button[contains(@class, "px-3 py-2 dropdown-btn")]/h2[contains(@class, "text-[#9B9B9B] text-[13px] whitespace-nowrap max-[350px]:truncate")]/text()',
            )
            .get()
            .split("-")[-1]
        )
        chaptername = (
            response.xpath(
                '//div[contains(@class, "dropdown md:w-[13em] max-[350px]:w-[10rem] ")]/button[contains(@class, "px-3 py-2 dropdown-btn")]/h2[contains(@class, "text-[#9B9B9B] text-[13px] whitespace-nowrap max-[350px]:truncate")]/text()',
            )
            .get()
            .split("-")[-0]
        )

        slug = f"{title} {chaptername}"
        loader.add_value("url", response.url)
        loader.add_value("chapterslug", slug)
        loader.add_value("chaptername", chaptername)
        if chaptername.lower() != chaptertitle.lower():
            loader.add_value("chaptertitle", chaptertitle)
        else:
            loader.add_value("chaptertitle", "")
        loader.add_value("image_urls", images)
        loader.add_value("updated_at", chapters_time)
        loader.add_value("comictitle", title)
        loader.add_xpath(
            "comicslug",
            "//div[@class='flex flex-col items-center space-y-2 pt-6 px-5 text-center']/p/a/span/text()",
        )
        item = loader.load_item()
        yield item
        logger.debug("A New Chapter was found at %s", response.url)
