import colorama
import scrapy


class SchlottererSpider(scrapy.Spider):
    name = 'schlotterer'
    allowed_domains = ['schlotterer.com']

    def __init__(self, *args, **kwargs):
        super(SchlottererSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://schlotterer.com/de/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        product_menu = response.css("ul.menu-main > li:first-child")
        categories = product_menu.css("ul.menu-main__sub-items.first-level > li")
        for category in categories:
            self.products.extend(
                category.css("li.menu-main__sub-item a.menu-main__sub-link ::text").getall()
            )
        self.logger.info(f"Products: {self.products}")
