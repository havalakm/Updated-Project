import colorama
import scrapy


class ScreenalSpider(scrapy.Spider):
    name = "omnika"
    allowed_domains = ["omnnika.com"]
    not_found = "__NOT_FOUND__"

    def __init__(self, *args, **kwargs):
        super(ScreenalSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://omnika.com/produkty"
        self.start_parse = self.parse_products
        # List of dict where each dict has key as product category and value as list of products
        self.products = []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):

        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")

        name = response.xpath('//p/text()').getall()

        self.products = [
            {'name': name}]

        self.logger.info(f"Products: {self.products}")