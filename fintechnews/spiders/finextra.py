import scrapy
from fintechnews.items import FintechnewsItem
import dateparser
import pytz

item = FintechnewsItem()


class FinextraSpider(scrapy.Spider):
    name = 'finextra'
    allowed_domains = ["finextra.com"]
    start_urls = ["https://www.finextra.com/latest-news"]

    def parse(self, response):
        articles = response.xpath("//div[@class='module--story']")

        for article in articles:
            category = article.xpath(
                "./div[@class='story--content']/h6/a/text()").get()
            if category:
                category = category.replace("/", "")
            else:
                continue
            article_link = article.xpath(
                "./div[@class='story--content']/h4/a/@href").get()
            title = article.xpath(
                "./div[@class='story--content']/h4/a/text()").get()
            title = title.replace("'", "\u2019")

            yield scrapy.Request(response.urljoin(article_link),
                                 cb_kwargs={'category': category,
                                            'article_link': article_link,
                                            'title': title},
                                 callback=self.parse_readmore)

        # next_page = response.xpath(
        #     "//div[@id='pagination']/a[last()-1]/@href").extract_first()
        # if next_page:
        #     yield response.follow(next_page,
        #                           callback=self.parse)

    def parse_readmore(self, response, category, article_link, title):
        item['category'] = category
        item['article_link'] = article_link
        item['title'] = title
        item['source'] = 'Finextra'

        date = response.xpath(
            "//div[@id='premierSectionChild']/div/div[2]/div[2]/div[2]/div/span/text()").get().strip()
        item['datetime'] = dateparser.parse(date).astimezone(pytz.utc)

        item['image'] = response.xpath(
            "//img[@id='ctl00_ctl00_body_mainContent_NewsActicle_imgNews']/@src").get()

        first = response.xpath(
            "//div[@class='article--body']/p[@class='stand-first']//text()")
        first_para = [f.get().strip() for f in first]
        first_para = ' '.join(first_para)
        body = response.xpath(
            "//div[@id='ctl00_ctl00_body_mainContent_NewsActicle_pnlBody']//text()")
        body_para = [b.get().strip() for b in body]
        body_para = ' '.join(body_para)

        item['desc'] = first_para + body_para

        yield item
