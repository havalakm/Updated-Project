import colorama
import scrapy


class WaremaSpider(scrapy.Spider):
    name = 'warema'
    allowed_domains = ['warema.de']

    def __init__(self, *args, **kwargs):
        super(WaremaSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://warema.de/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        product_menus = response.css("div.topNavIcons")
        self.products += product_menus.css("div.swiper-slide div.swiper-title::text").getall()
        self.logger.info(f"Products: {self.products}")
