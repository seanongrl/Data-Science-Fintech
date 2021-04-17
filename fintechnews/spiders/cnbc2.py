import scrapy
from fintechnews.items import FintechnewsItem
import unicodedata
from datetime import datetime
import pytz

item = FintechnewsItem()


class CNBCSpider(scrapy.Spider):
    name = 'cnbc2'
    allowed_domains = ["cnbc.com"]
    start_urls = ["https://www.cnbc.com/world/?region=world"]

    def parse(self, response):
        articles = response.xpath("//div[@class='RiverPlusCard-container']")
        print(len(articles))
        for article in articles:
            link = article.xpath(".//a/@href").get()

            yield scrapy.Request(response.urljoin(link),
                                 cb_kwargs={'link': link},
                                 callback=self.parse_readmore)

    def parse_readmore(self, response, link):
        item['article_link'] = link
        item['source'] = 'CNBC'
        item['image'] = None

        item['title'] = response.xpath("//h1[@class='ArticleHeader-headline']/text()").get()
        if item['title'] is None:
            item['title'] = response.xpath("//h1[@class='ArticleHeader-styles-makeit-headline--1DSjp']/text()").get()

        item['category'] = response.xpath(
            "//a[@class='ArticleHeader-eyebrow']/text()").get()
        if item['category'] is None:
            item['category'] = response.xpath("//a[@class='ArticleHeader-styles-makeit-eyebrow--2XyZs']/text()").get()

        text = ' '.join(
            response.xpath("//div[@class='group']//*/text()").getall())
        text = unicodedata.normalize("NFKD", text)
        item['desc'] = text

        timestamp = ' '.join(response.xpath("//time[@data-testid='published-timestamp']/text()").getall())
        timestamp = timestamp[15:-4]  # remove unnecessary characters
        timestamp = datetime.strptime(timestamp, "%b %d %Y %I:%M %p")
        tz = pytz.timezone('US/Eastern')  # creating a timezone object
        timestamp = tz.localize(timestamp)  # assign EST timezone to extracted datetime
        timestamp = timestamp.astimezone(pytz.utc)  # convert/display as UTC
        item['datetime'] = timestamp

        yield item
