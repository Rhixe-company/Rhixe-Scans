# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dateparser import parse
from django.template.defaultfilters import slugify
from itemloaders.processors import MapCompose
from itemloaders.processors import TakeFirst
from scrapy.item import Field
from scrapy.item import Item
from w3lib.html import remove_comments
from w3lib.html import remove_tags
from w3lib.html import strip_html5_whitespace


def gen_slug(value):
    object = slugify(value)
    return object.strip()


def get_slug(value):
    object = value.split("/")[-1].split("-")[-0]
    return object.strip()


def get_des(value):
    object = (
        value.replace("\\n", "")
        .replace("\r", "")
        .replace("\\r", "")
        .replace("rn", "")
        .replace("rnrnxa0 ", "")
        .replace("kindness.", "")
        .replace("\xa0", "")
        .replace("\\xa0", "")
        .replace("//", "")
        .replace("\\", "")
        .replace("\\", "")
        .replace("\n", "")
        .replace("/n", "")
        .replace("['", "")
        .replace("']", "")
        .replace("'", "")
    )
    # ob = "[] ".join(map(str, object))
    ob = object

    return ob.strip()


def get_date(value):
    object = parse(value, languages=["en"], date_formats=["%d/%m/%Y"]).date()
    return object


def get_html(value):
    object = remove_tags(value)
    return object.strip()


# def join_array(value):
#     object = ", ".join(map(str, value))
#     return object.strip()


def join_array(value):
    object = value.split("-")[-0]
    return object.strip()


def join_array2(value):
    object = value.split("-")[-1]
    return object.strip()


def strip_html(value):
    object = strip_html5_whitespace(value)
    return object.strip()


def comments_html(value):
    object = remove_comments(value)
    return object.strip()


class ComicItem(Item):
    title = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    description = Field(
        input_processor=MapCompose(get_des, strip_html, comments_html, get_html),
        output_processor=TakeFirst(),
    )
    slug = Field(input_processor=MapCompose(gen_slug), output_processor=TakeFirst())

    rating = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    status = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    type = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    updated_at = Field(
        input_processor=MapCompose(get_date),
        output_processor=TakeFirst(),
    )
    serialization = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )

    author = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    artist = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    genres = Field(
        input_processor=MapCompose(get_html),
    )
    numChapters = Field(output_processor=TakeFirst())
    crawled = Field(output_processor=TakeFirst())
    # downloaded_at = Field(
    #     output_processor=TakeFirst(),
    # )
    url = Field(output_processor=TakeFirst())
    spider = Field(output_processor=TakeFirst())
    image_urls = Field()
    images = Field()


class ChapterItem(Item):
    comictitle = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    comicslug = Field(
        input_processor=MapCompose(gen_slug),
        output_processor=TakeFirst(),
    )
    chaptertitle = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    chaptername = Field(
        input_processor=MapCompose(get_html),
        output_processor=TakeFirst(),
    )
    chapterslug = Field(
        input_processor=MapCompose(gen_slug, get_html),
        output_processor=TakeFirst(),
    )
    updated_at = Field(
        input_processor=MapCompose(get_date),
        output_processor=TakeFirst(),
    )
    # numPages = Field(output_processor=TakeFirst())
    # downloaded_at = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    spider = Field(output_processor=TakeFirst())
    image_urls = Field()
    images = Field()
