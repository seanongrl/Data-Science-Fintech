import scrapy


class FintechnewsBlogSpider(scrapy.Spider):
    name = 'fintechnews_blog'
    allowed_domains = ['fintechnews.sg']
    start_urls = ['https://fintechnews.sg/blog/']

    titles = []
    categories = []
    descs = []
    datetimes = []
    sources = []

    def parse(self, response):
        print("processing:" + response.url)

        all_articles = response.xpath("//div[@class='article-list']//div[@class='item-content']")

        for article in all_articles:

            self.titles.append(article.xpath(".//h3[@class='entry-title']/a/text()").get())

            category = article.xpath(".//div[@class='content-category']/a/text()").getall()
            if len(category) > 1:
                category = [', '.join(category)]
            self.categories.append(category)

            # access read more links
            read_more = article.xpath(".//a[@class='read-more-link']/@href").get()
            print("read more", read_more)
            yield scrapy.Request(response.urljoin(read_more), callback=self.parse_readmore)
            print("after yield")

    def parse_readmore(self, response):
        print("\n\n*******************  at readmore")
        # main article
        words = response.xpath("//div[@class='pf-content']//p/text()").getall()
        article = ''.join(words)
        self.descs.append(article)

        # source and datetime
        span = response.xpath("//div[@class='article-header']/span/span/a/text()").getall()

        author = span[0]
        self.sources.append(author)

        timestamp = span[1]
        self.datetimes.append(timestamp)
        print(self.sources)
