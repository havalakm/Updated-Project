import colorama
import scrapy


class SeltSpider(scrapy.Spider):
    name = 'selt'
    allowed_domains = ['selt.com']
    start_urls = ['http://selt.com/']

    def __init__(self, *args, **kwargs):
        super(SeltSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://www.selt.com/produkty-de"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        self.products += [
            x.strip()
            for x in response.css(
                "div.menu > ul.poziom1 > li:nth-child(2) > ul > li > a::text"
            ).getall()
            if x.strip()
        ]
        self.logger.info(f"Products: {self.products}")
