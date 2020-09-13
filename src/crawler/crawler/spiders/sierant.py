import colorama
import scrapy


class SierantSpider(scrapy.Spider):
    name = 'sierant'
    allowed_domains = ['sierant.pl']

    def __init__(self, *args, **kwargs):
        super(SierantSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://www.sierant.pl/de/unsere-produkte-t174"
        self.start_parse = self.parse_product_links
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_product_links(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        product_links = response.css("section.produkty-box li > div > a::attr(href)").getall()
        self.logger.info(f"Product Links: {product_links}")
        for link in product_links:
            yield response.follow(url=link, callback=self.parse_products)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        self.products += [
            x.strip()
            for x in response.css("div.prod-item div.prod-item-content h2::text").getall()
        ]
        self.logger.info(f"Products: {self.products}")
