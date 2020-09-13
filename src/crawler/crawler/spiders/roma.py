import colorama
import scrapy


class RomaSpider(scrapy.Spider):
    name = 'roma'
    allowed_domains = ['roma.de']

    def __init__(self, *args, **kwargs):
        super(RomaSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://roma.de/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        navigation_section = response.css("div.main-navigation-container")
        product_menu = navigation_section.css("li.menu-item.has-subnavigation:first-child")
        self.products += product_menu.css("li a ::text").getall()
        self.logger.info(f"Products: {self.products}")

