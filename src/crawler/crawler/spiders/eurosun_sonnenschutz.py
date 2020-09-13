import colorama
import scrapy


class EurosunSonnenschutzSpider(scrapy.Spider):
    name = 'eurosun_sonnenschutz'
    allowed_domains = ['eurosun-sonnenschutz.com']

    def __init__(self, *args, **kwargs):
        super(EurosunSonnenschutzSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://eurosun-sonnenschutz.com/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        main_navigation = response.css("div.nav-item")
        product_menu = main_navigation.pop(0)
        self.products += [x.strip() for x in product_menu.css("li a::text").getall()]
        self.logger.info(f"Products: {self.products}")
