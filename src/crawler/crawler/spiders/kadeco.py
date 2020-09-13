import colorama
import scrapy


class KadecoSpider(scrapy.Spider):
    name = 'kadeco'
    allowed_domains = ['kadeco.de']

    def __init__(self, *args, **kwargs):
        super(KadecoSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://kadeco.de/en/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        product_menu = response.css("li.submenu.products.sibling ul.level_2")
        self.products += [
            x.strip()
            for x in product_menu.css("li ::text").getall()
            if x.strip()
        ]
        self.logger.info(f"Products: {self.products}")
