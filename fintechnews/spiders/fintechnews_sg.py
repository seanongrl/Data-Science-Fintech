import scrapy
from fintechnews.items import FintechnewsItem
from datetime import datetime
import unicodedata
import pytz

item = FintechnewsItem()


class FintechnewssgSpider(scrapy.Spider):
    name = 'fintechnewssg'
    allowed_domains = ['fintechnews.sg']
    start_urls = ['https://fintechnews.sg/blog/']

    def parse(self, response):
        all_articles = response.xpath(
            "//div[@class='article-list']//div[@class='item-content']")

        for article in all_articles:
            item['title'] = article.xpath(
                ".//h3[@class='entry-title']/a/text()").get()
            item['category'] = article.xpath(
                ".//div[@class='content-category']/a/text()").getall()
            item['article_link'] = article.xpath(
                ".//a[@class='read-more-link']/@href").get()

            # yield 1 item set to pipeline for each category in each article
            for c in item['category']:
                yield scrapy.Request(response.urljoin(item['article_link']),
                                     callback=self.parse_readmore,
                                     meta={'title': item['title'],
                                           'category': c,
                                           'article_link': item[
                                               'article_link']})

        # next_page = response.xpath(
        #     "//div[@class='pagination']/a[@class='next page-numbers']/@href").get()
        # if next_page:
        #     yield scrapy.Request(response.urljoin(next_page),
        #                          callback=self.parse)

    def parse_readmore(self, response):
        item['title'] = response.meta.get('title')
        item['category'] = response.meta.get('category')
        item['article_link'] = response.meta.get('article_link')

        words = ' '.join(response.xpath("//div[@class='pf-content']//p//text()").getall())
        words = unicodedata.normalize("NFKD", words)
        item['desc'] = words

        item['image'] = response.xpath(
            "//div[@class='article-header']/img/@src").get()

        span = response.xpath(
            "//div[@class='article-header']/span/span/a/text()").getall()

        item['source'] = span[0]

        published_date = datetime.strptime(span[1], "%B %d, %Y")
        if published_date.date() == datetime.today().date():
            item['datetime'] = datetime.now().astimezone(pytz.utc)
        else:
            item['datetime'] = published_date.astimezone(pytz.utc)

        yield item
