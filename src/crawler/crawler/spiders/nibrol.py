import colorama
import scrapy


class NibrolSpider(scrapy.Spider):
    name = 'nibrol'
    allowed_domains = ['nibrol.com']

    def __init__(self, *args, **kwargs):
        super(NibrolSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://nibrol.com/"
        self.start_parse = self.parse_products
        self.products = []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        menu_container = response.css("div.menu-floating-menu-container")
        product_section = menu_container.css("li#menu-item-623")
        self.products = product_section.css("ul.sub-menu li a::text").getall()
        self.products = [x.strip() for x in self.products]
        self.logger.info(f"Products: {self.products}")

