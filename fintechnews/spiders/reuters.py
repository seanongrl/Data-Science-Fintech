import scrapy
from fintechnews.items import FintechnewsItem
import dateparser
import pytz
from datetime import datetime, timedelta

item = FintechnewsItem()


class FinextraSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ["reuters.com"]
    start_urls = ["https://www.reuters.com/news/archive/worldnews?view=page&page=1&pageSize=10",
                  "https://www.reuters.com/news/archive/businessnews?view=page&page=1&pageSize=10",
                  "https://www.reuters.com/news/archive/marketsNews?view=page&page=1&pageSize=10",
                  "https://www.reuters.com/news/archive/mcbreakingviews?view=page&page=1&pageSize=10",
                  "https://www.reuters.com/news/archive/technologynews?view=page&page=1&pageSize=10"]

    def parse(self, response):
        articles = response.xpath("//article[@class='story ']")

        for article in articles:
            title = article.xpath(".//h3[@class='story-title']/text()").get().strip()
            title = title.replace("'", "\u2019")
            article_link = article.xpath(".//div[@class='story-content']/a/@href").get()
            image = article.xpath(".//div[@class='story-photo lazy-photo ']//img/@org-src").get()

            articletime = article.xpath(".//span[@class='timestamp']/text()").get()
            articletime = dateparser.parse(articletime)
            if articletime.tzinfo is not None:  # occurs within last 24h
                sgtime = datetime.now()
                sgtimezone = pytz.timezone('Asia/Kuala_Lumpur')
                sgtime = sgtimezone.localize(sgtime)
                if articletime > sgtime:
                    articletime = articletime - timedelta(days=1)

            yield scrapy.Request(response.urljoin(article_link),
                                 cb_kwargs={'title': title,
                                            'article_link': article_link,
                                            'image': image,
                                            'articletime': articletime},
                                 callback=self.parse_readmore)

        # next_page = response.xpath(
        #     "//div[@class='control-nav']/a[@class='control-nav-next']/@href").get()
        # if next_page:
        #     yield response.follow(next_page,
        #                           callback=self.parse)

    def parse_readmore(self, response, title, article_link, image, articletime):
        item['title'] = title
        item['article_link'] = article_link
        item['image'] = image
        item['datetime'] = articletime
        item['source'] = 'Reuters'
        item['category'] = response.xpath("//div[@class='ArticleHeader-info-container-3-6YG']/a/text()").get()

        text = response.xpath("//p[@class='Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x']/text()").getall()
        item['desc'] = ' '.join(text)

        yield item
