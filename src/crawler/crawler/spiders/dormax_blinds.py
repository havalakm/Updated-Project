import colorama
import scrapy


class DormaxBlindsSpider(scrapy.Spider):
    name = 'dormax-blinds'
    allowed_domains = ['dormax-blinds.pl']

    def __init__(self, *args, **kwargs):
        super(DormaxBlindsSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://www.dormax-blinds.pl/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        products = response.css(
            "div#menu_left > ul > li > a ::text"
        ).getall()
        self.products += [x.strip() for x in products if x.strip()]
        self.logger.info(f"Products: {self.products}")
