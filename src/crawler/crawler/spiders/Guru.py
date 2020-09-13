import colorama
import scrapy


class ScreenalSpider(scrapy.Spider):
    name = "guru"
    allowed_domains = ["guru-mc.com"]
    not_found = "__NOT_FOUND__"

    def __init__(self, *args, **kwargs):
        super(ScreenalSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://guru-mc.com/"
        self.start_parse = self.parse_products
        # List of dict where each dict has key as product category and value as list of products
        self.products = []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")

        products = [item.strip() for item in response.xpath('//a/text()').extract() if item.strip()]
        content = response.xpath('//h3/text()').getall()
        paragraph = [item.strip() for item in response.xpath('//p/text()').extract() if item.strip()]
        # paragraph = response.xpath('//p/text()').extract_first().strip()
        # self.paragraph = [x.strip() for x in self.products if x.strip()]
        #self.paragraph = response.xpath("//p/text()").getall()
        #self.paragraph = [x.strip() for x in self.products if x.strip()]
        #self.logger.info(f"paragraph: {self.paragraph}")

        self.products = [
            {'products': products,
             'content': content,
             'paragraph': paragraph
             }
        ]
        self.logger.info(f"Products: {self.products}")