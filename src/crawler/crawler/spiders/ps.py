import colorama
import scrapy


class ScreenalSpider(scrapy.Spider):
    name = "ps"
    allowed_domains = ["psprojektundstrategie.de"]
    not_found = "__NOT_FOUND__"

    def __init__(self, *args, **kwargs):
        super(ScreenalSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://www.psprojektundstrategie.de/"
        self.start_parse = self.parse_products
        # List of dict where each dict has key as product category and value as list of products
        self.products = []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")

        menu = response.xpath('//ul/li/a/div/div/p/text()').getall()
        text = response.xpath('//*[@id="comp-ilrqrgh7"]/p[1]/span/text()').getall()
        motivation = response.xpath('//*[@id="comp-ilf610ir"]/h4/span/text()').getall()
        paragraph = response.xpath('//*[@id="comp-ilf6nccg"]/p/text()').getall()
        acheivements = response.xpath('//*[@id="comp-ilrqfj0h"]/h4/span/text()').getall()
        p = response.xpath('//*[@id="comp-ilrqfj0m"]/p/span[1]/span/text()').getall()
        communication = response.xpath('//ul/li/p/span/span/text()').getall()
        reference = response.xpath('//div/p/span/span/span/text()').getall()
        reference1 = response.xpath('//div/p/span/text()').getall()
        reference2 = response.xpath('//div/p/span/span/text()').getall()

        self.products = [
            {'menu': menu,
             'motivation': motivation,
             'text': text,
             'paragraph': paragraph,
             'acheivements': acheivements,
             'p': p,
             'communication': communication,
             'reference': reference,
             'reference1': reference1,
             'reference2': reference2}]

        self.logger.info(f"Products: {self.products}")
