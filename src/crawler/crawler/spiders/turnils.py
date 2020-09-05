import colorama
import scrapy


class TurnilsSpider(scrapy.Spider):
    name = 'turnils'
    allowed_domains = ['turnils.com']
    start_urls = ['']

    def __init__(self, *args, **kwargs):
        super(TurnilsSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://turnils.com/"
        self.start_parse = self.parse_products
        self.products = []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        home_page_menu = response.css("ul.gf-menu.l1")
        product_menu = home_page_menu.css("li.item101.parent")
        self.products = product_menu.css("ul.l2 li a::text").getall()
        self.products = [x.strip() for x in self.products]
        self.logger.info(f"Products: {self.products}")

