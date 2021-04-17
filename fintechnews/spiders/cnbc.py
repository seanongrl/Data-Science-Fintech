import scrapy
from fintechnews.items import FintechnewsItem
import unicodedata
import dateparser
import pytz

item = FintechnewsItem()


class CNBCSpider(scrapy.Spider):
    name = 'cnbc'
    allowed_domains = ["cnbc.com"]
    start_urls = ["https://www.cnbc.com/world/?region=world"]

    def parse(self, response):
        articles = response.xpath("//div[@class='LatestNews-newsFeed']")

        for article in articles:
            headline = article.xpath(
                ".//div[@class='LatestNews-headline']/a/@title").get()
            headline = headline.replace("'", "\u2019")
            link = article.xpath(
                ".//div[@class='LatestNews-headline']/a/@href").get()
            timestamp = article.xpath(
                ".//div[@class='LatestNews-timestamp']/text()").get()

            yield scrapy.Request(response.urljoin(link),
                                 cb_kwargs={'headline': headline,
                                            'link': link,
                                            'timestamp': timestamp},
                                 callback=self.parse_readmore)

    def parse_readmore(self, response, headline, link, timestamp):
        item['title'] = headline
        item['article_link'] = link
        item['datetime'] = dateparser.parse(timestamp).astimezone(pytz.utc)
        item['source'] = 'CNBC'
        item['image'] = None

        item['category'] = response.xpath("//a[@class='ArticleHeader-eyebrow']/text()").get()
        if item['category'] is None:
            item['category'] = response.xpath("//a[@class='ArticleHeader-styles-makeit-eyebrow--2XyZs']/text()").get()

        text = ' '.join(
            response.xpath("//div[@class='group']//*/text()").getall())
        text = unicodedata.normalize("NFKD", text)
        item['desc'] = text

        yield item
