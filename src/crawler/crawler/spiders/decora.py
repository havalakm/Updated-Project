import colorama
import scrapy


class DecoraSpider(scrapy.Spider):
    name = 'decora'
    allowed_domains = ['decora.co.uk']

    def __init__(self, *args, **kwargs):
        super(DecoraSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://decora.co.uk/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        menu_container = response.css("div.menu_container")
        product_section = menu_container.css("nav#primary_nav_wrap ul li:first-child ul")
        products = product_section.css("li a::text").getall()
        self.products += [x.strip() for x in products]
        self.logger.info(f"Products: {self.products}")
