import scrapy
from bs4 import BeautifulSoup


class MySpider(scrapy.Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract data using BeautifulSoup
        title = soup.find("title").text
        links = [a["href"] for a in soup.find_all("a")]
        # Yield items or requests as needed
        yield {"title": title, "links": links}
