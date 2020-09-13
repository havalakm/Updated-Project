import colorama
import scrapy


class NyffeneggerSpider(scrapy.Spider):
    name = 'nyffenegger'
    allowed_domains = ['nyffenegger.ch']

    def __init__(self, *args, **kwargs):
        super(NyffeneggerSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://nyffenegger.ch/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        product_menu = response.css("div.navigation > nav.main > ul > li:first-child")
        self.products += [
            x.strip()
            for x in product_menu.css("li > a ::text").getall()
        ]
        self.logger.info(f"Products: {self.products}")
