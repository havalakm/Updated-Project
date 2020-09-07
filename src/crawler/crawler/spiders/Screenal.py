import colorama
import scrapy


class ScreenalSpider(scrapy.Spider):
    name = "screenal"
    allowed_domains = ["screenal.com"]
    not_found = "__NOT_FOUND__"

    def __init__(self, *args, **kwargs):
        super(ScreenalSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://www.screenal.gr/en/product_category/insect-screens/"
        self.start_parse = self.parse_products
        # List of dict where each dict has key as product category and value as list of products
        self.products = []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")

        insects = response.xpath('//h4/a/text()').getall()

        yield {'titles': insects}
