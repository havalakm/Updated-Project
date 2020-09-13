import colorama
import scrapy


class LamexSpider(scrapy.Spider):
    name = 'lamex'
    allowed_domains = ['lamex.ch']

    def __init__(self, *args, **kwargs):
        super(LamexSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://lamex.ch/de/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        product_menu = response.css("ul.nav.navbar-nav > li:nth-child(2) > ul.dropdown-menu")
        self.products += product_menu.css("li ::text").getall()[1:-1]
        self.logger.info(f"Products: {self.products}")
